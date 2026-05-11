#!/usr/bin/env python3
"""
Automated checks for CIS AWS Compute controls related to Amazon ECS.

Controls addressed:
- 3.1 Ensure task definitions using 'host' network mode do not allow
      privileged or root user access
- 3.2 Ensure 'assignPublicIp' is set to 'DISABLED' for ECS services

Credentials/region are picked up from the standard AWS SDK resolution chain
and environment variables.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import os

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError


# -----------------------------
# Data models
# -----------------------------


@dataclass
class CheckFinding:
    resource_arn: str
    reason: str
    details: Optional[Dict] = None


@dataclass
class CheckResult:
    passed: bool
    findings: List[CheckFinding]

    def to_dict(self) -> Dict:
        return {
            "passed": self.passed,
            "findings": [
                {
                    "resource_arn": f.resource_arn,
                    "reason": f.reason,
                    "details": f.details,
                }
                for f in self.findings
            ],
        }


# -----------------------------
# Helpers
# -----------------------------


def _build_ecs_client(region: Optional[str]) -> any:
    boto_cfg = Config(retries={"max_attempts": 10, "mode": "standard"})
    return boto3.client("ecs", region_name=region, config=boto_cfg)


def _chunked(items: List[str], size: int) -> List[List[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def _is_root_user_value(user_value: str) -> bool:
    if not user_value:
        return False
    candidate = str(user_value).strip().lower()
    if candidate == "root" or candidate == "0":
        return True
    # Handle formats like "0:0" or "root:root" or "1000:0"
    if ":" in candidate:
        uid = candidate.split(":", 1)[0]
        return uid in {"0", "root"}
    return False


# -----------------------------
# Checks
# -----------------------------


def ecs_task_definitions_host_mode_no_privileged_root(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any task definition with networkMode == 'host' has a container
    with privileged == True or user effectively root.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                if task_def.get("networkMode") != "host":
                    continue

                for cdef in task_def.get("containerDefinitions", []):
                    privileged = bool(cdef.get("privileged", False))
                    user_value = cdef.get("user")
                    is_root = _is_root_user_value(user_value) if user_value else False

                    if privileged or is_root:
                        findings.append(
                            CheckFinding(
                                resource_arn=arn,
                                reason="Container allows privileged or root user in host mode",
                                details={
                                    "containerName": cdef.get("name"),
                                    "privileged": privileged,
                                    "user": user_value,
                                },
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_services_assign_public_ip_disabled(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any ECS service configured with awsvpc networking has
    assignPublicIp != 'DISABLED'. If awsvpcConfiguration is absent,
    the item is treated as NotApplicable and not a failure.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        clusters: List[str] = []
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            clusters.extend(page.get("clusterArns", []))

        for cluster_arn in clusters:
            service_arns: List[str] = []
            svc_paginator = client.get_paginator("list_services")
            for page in svc_paginator.paginate(cluster=cluster_arn):
                service_arns.extend(page.get("serviceArns", []))

            for batch in _chunked(service_arns, 10):
                if not batch:
                    continue
                try:
                    resp = client.describe_services(cluster=cluster_arn, services=batch)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=cluster_arn,
                            reason="Error describing ECS services",
                            details={"error": str(e), "services": batch},
                        )
                    )
                    continue

                for svc in resp.get("services", []):
                    svc_arn = svc.get("serviceArn", "unknown")
                    awsvpc = (
                        (svc.get("networkConfiguration") or {})
                        .get("awsvpcConfiguration")
                    )

                    if not awsvpc:
                        # Not applicable (bridge/host or EC2 service without awsvpc)
                        continue

                    assign_public_ip = awsvpc.get("assignPublicIp")
                    if assign_public_ip != "DISABLED":
                        findings.append(
                            CheckFinding(
                                resource_arn=svc_arn,
                                reason="assignPublicIp is not DISABLED",
                                details={
                                    "clusterArn": cluster_arn,
                                    "assignPublicIp": assign_public_ip,
                                },
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing clusters/services failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


# Additional ECS checks


def ecs_task_definitions_no_pid_mode_host(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any task definition has pidMode == 'host'.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                if task_def.get("pidMode") == "host":
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="pidMode is set to 'host'",
                            details={"pidMode": task_def.get("pidMode")},
                        )
                    )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_definitions_privileged_false(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any containerDefinition within any task definition has privileged == True.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                for cdef in task_def.get("containerDefinitions", []):
                    if bool(cdef.get("privileged", False)):
                        findings.append(
                            CheckFinding(
                                resource_arn=arn,
                                reason="Container has 'privileged' set to true",
                                details={"containerName": cdef.get("name")},
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_definitions_readonly_root_filesystem_enabled(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any containerDefinition does not have readonlyRootFilesystem == True.
    Missing value is treated as False per default behavior.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                for cdef in task_def.get("containerDefinitions", []):
                    if cdef.get("readonlyRootFilesystem") is not True:
                        findings.append(
                            CheckFinding(
                                resource_arn=arn,
                                reason="Container readonlyRootFilesystem is not enabled",
                                details={
                                    "containerName": cdef.get("name"),
                                    "readonlyRootFilesystem": cdef.get("readonlyRootFilesystem"),
                                },
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_definitions_no_secrets_in_environment(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any containerDefinition has environment entries whose names match
    known sensitive keys (e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    ECS_ENGINE_AUTH_DATA).
    """
    sensitive_names = {
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "ECS_ENGINE_AUTH_DATA",
    }

    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                for cdef in task_def.get("containerDefinitions", []):
                    env = cdef.get("environment") or []
                    for pair in env:
                        name = (pair.get("name") or "").strip()
                        if name in sensitive_names:
                            findings.append(
                                CheckFinding(
                                    resource_arn=arn,
                                    reason="Sensitive variable present in environment",
                                    details={
                                        "containerName": cdef.get("name"),
                                        "name": name,
                                    },
                                )
                            )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_definitions_logging_configured(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if no containerDefinition in a task definition has a logConfiguration
    with a non-empty logDriver.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                containers = task_def.get("containerDefinitions", [])
                has_logging = False
                for cdef in containers:
                    log_cfg = cdef.get("logConfiguration") or {}
                    if (log_cfg.get("logDriver") or "").strip():
                        has_logging = True
                        break

                if not has_logging:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="No container has logConfiguration.logDriver set",
                        )
                    )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_fargate_services_use_latest_platform(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any Fargate service does not use platformVersion LATEST.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        clusters: List[str] = []
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            clusters.extend(page.get("clusterArns", []))

        for cluster_arn in clusters:
            service_arns: List[str] = []
            svc_paginator = client.get_paginator("list_services")
            for page in svc_paginator.paginate(cluster=cluster_arn):
                service_arns.extend(page.get("serviceArns", []))

            for batch in _chunked(service_arns, 10):
                if not batch:
                    continue
                try:
                    resp = client.describe_services(cluster=cluster_arn, services=batch)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=cluster_arn,
                            reason="Error describing ECS services",
                            details={"error": str(e), "services": batch},
                        )
                    )
                    continue

                for svc in resp.get("services", []):
                    svc_arn = svc.get("serviceArn", "unknown")
                    launch_type = svc.get("launchType")
                    if launch_type != "FARGATE":
                        # Not a Fargate service; skip
                        continue
                    platform_version = (svc.get("platformVersion") or "").strip()
                    if platform_version != "LATEST":
                        findings.append(
                            CheckFinding(
                                resource_arn=svc_arn,
                                reason="Fargate platformVersion is not LATEST",
                                details={
                                    "clusterArn": cluster_arn,
                                    "platformVersion": platform_version,
                                },
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing clusters/services failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_definitions_trusted_image_registries(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any container image does not originate from trusted registries.

    Trusted registry prefixes can be configured via the environment variable
    ECS_TRUSTED_IMAGE_PREFIXES as a comma-separated list, e.g.:
      public.ecr.aws,123456789012.dkr.ecr.us-east-1.amazonaws.com,my-registry.example.com/

    Defaults trust to Amazon ECR (public and private):
      - public.ecr.aws/
      - *.dkr.ecr.*.amazonaws.com
    """
    env_val = os.getenv("ECS_TRUSTED_IMAGE_PREFIXES", "").strip()
    trusted_prefixes: List[str] = [p.strip() for p in env_val.split(",") if p.strip()]
    # Add defaults for AWS ECR if user didn't specify anything
    use_defaults = len(trusted_prefixes) == 0
    if use_defaults:
        trusted_prefixes = [
            "public.ecr.aws/",
        ]

    def _is_trusted(image: str) -> bool:
        if not image:
            return False
        # Explicit prefixes
        for pref in trusted_prefixes:
            if image.startswith(pref):
                return True
        # Generic AWS ECR private
        if ".dkr.ecr." in image and image.endswith(".amazonaws.com"):
            return True
        return False

    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    resp = client.describe_task_definition(taskDefinition=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error describing task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                task_def = resp.get("taskDefinition", {})
                for cdef in task_def.get("containerDefinitions", []):
                    image = (cdef.get("image") or "").strip()
                    if not _is_trusted(image):
                        findings.append(
                            CheckFinding(
                                resource_arn=arn,
                                reason="Container image not from trusted registry",
                                details={
                                    "containerName": cdef.get("name"),
                                    "image": image,
                                    "trustedPrefixes": trusted_prefixes,
                                    "defaultsApplied": use_defaults,
                                },
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_sets_assign_public_ip_disabled(
    region: Optional[str] = None,
) -> CheckResult:
    """
    Fails if any ECS task set under any service has awsvpcConfiguration.assignPublicIp != 'DISABLED'.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        clusters: List[str] = []
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            clusters.extend(page.get("clusterArns", []))

        for cluster_arn in clusters:
            service_arns: List[str] = []
            svc_paginator = client.get_paginator("list_services")
            for page in svc_paginator.paginate(cluster=cluster_arn):
                service_arns.extend(page.get("serviceArns", []))

            for batch in _chunked(service_arns, 10):
                if not batch:
                    continue
                try:
                    svc_resp = client.describe_services(cluster=cluster_arn, services=batch)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=cluster_arn,
                            reason="Error describing ECS services",
                            details={"error": str(e), "services": batch},
                        )
                    )
                    continue

                for svc in svc_resp.get("services", []):
                    svc_arn = svc.get("serviceArn", "unknown")
                    try:
                        ts_resp = client.describe_task_sets(
                            cluster=cluster_arn, service=svc_arn
                        )
                    except (ClientError, BotoCoreError) as e:
                        findings.append(
                            CheckFinding(
                                resource_arn=svc_arn,
                                reason="Error describing task sets",
                                details={"error": str(e)},
                            )
                        )
                        continue

                    for ts in ts_resp.get("taskSets", []):
                        ts_arn = ts.get("taskSetArn", "unknown")
                        awsvpc = (
                            (ts.get("networkConfiguration") or {})
                            .get("awsvpcConfiguration")
                        )
                        if not awsvpc:
                            continue
                        assign_public_ip = awsvpc.get("assignPublicIp")
                        if assign_public_ip != "DISABLED":
                            findings.append(
                                CheckFinding(
                                    resource_arn=ts_arn,
                                    reason="assignPublicIp is not DISABLED for task set",
                                    details={
                                        "clusterArn": cluster_arn,
                                        "serviceArn": svc_arn,
                                        "assignPublicIp": assign_public_ip,
                                    },
                                )
                            )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing clusters/services/task sets failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_services_tagged(region: Optional[str] = None) -> CheckResult:
    """
    Fails if any ECS service has zero customer (non aws:) tags.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        clusters: List[str] = []
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            clusters.extend(page.get("clusterArns", []))

        for cluster_arn in clusters:
            service_arns: List[str] = []
            svc_paginator = client.get_paginator("list_services")
            for page in svc_paginator.paginate(cluster=cluster_arn):
                service_arns.extend(page.get("serviceArns", []))

            for batch in _chunked(service_arns, 10):
                if not batch:
                    continue
                for svc_arn in batch:
                    try:
                        tag_resp = client.list_tags_for_resource(resourceArn=svc_arn)
                    except (ClientError, BotoCoreError) as e:
                        findings.append(
                            CheckFinding(
                                resource_arn=svc_arn,
                                reason="Error listing tags for service",
                                details={"error": str(e)},
                            )
                        )
                        continue

                    tags = tag_resp.get("tags", [])
                    user_tags = [t for t in tags if not (t.get("key", "").startswith("aws:"))]
                    if len(user_tags) == 0:
                        findings.append(
                            CheckFinding(
                                resource_arn=svc_arn,
                                reason="Service has no non aws: tags",
                                details={"tags": tags},
                            )
                        )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing clusters/services failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_clusters_tagged(region: Optional[str] = None) -> CheckResult:
    """
    Fails if any ECS cluster has zero customer (non aws:) tags.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        clusters: List[str] = []
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            clusters.extend(page.get("clusterArns", []))

        for cluster_arn in clusters:
            try:
                tag_resp = client.list_tags_for_resource(resourceArn=cluster_arn)
            except (ClientError, BotoCoreError) as e:
                findings.append(
                    CheckFinding(
                        resource_arn=cluster_arn,
                        reason="Error listing tags for cluster",
                        details={"error": str(e)},
                    )
                )
                continue

            tags = tag_resp.get("tags", [])
            user_tags = [t for t in tags if not (t.get("key", "").startswith("aws:"))]
            if len(user_tags) == 0:
                findings.append(
                    CheckFinding(
                        resource_arn=cluster_arn,
                        reason="Cluster has no non aws: tags",
                        details={"tags": tags},
                    )
                )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing clusters failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)


def ecs_task_definitions_tagged(region: Optional[str] = None) -> CheckResult:
    """
    Fails if latest revision of any task definition has zero customer (non aws:) tags.
    """
    client = _build_ecs_client(region)
    findings: List[CheckFinding] = []

    try:
        paginator = client.get_paginator("list_task_definitions")
        for page in paginator.paginate():
            task_arns: List[str] = page.get("taskDefinitionArns", [])
            for arn in task_arns:
                try:
                    tag_resp = client.list_tags_for_resource(resourceArn=arn)
                except (ClientError, BotoCoreError) as e:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Error listing tags for task definition",
                            details={"error": str(e)},
                        )
                    )
                    continue

                tags = tag_resp.get("tags", [])
                user_tags = [t for t in tags if not (t.get("key", "").startswith("aws:"))]
                if len(user_tags) == 0:
                    findings.append(
                        CheckFinding(
                            resource_arn=arn,
                            reason="Task definition has no non aws: tags",
                            details={"tags": tags},
                        )
                    )
    except (ClientError, BotoCoreError) as e:
        findings.append(
            CheckFinding(
                resource_arn="ecs",
                reason="Listing task definitions failed",
                details={"error": str(e)},
            )
        )

    return CheckResult(passed=len(findings) == 0, findings=findings)

# -----------------------------
# CLI
# -----------------------------


def _run_cli(region: Optional[str]) -> int:
    results: List[Tuple[str, CheckResult]] = []

    results.append(
        (
            "ecs_task_definitions_host_mode_no_privileged_root",
            ecs_task_definitions_host_mode_no_privileged_root(region=region),
        )
    )
    results.append(
        (
            "ecs_services_assign_public_ip_disabled",
            ecs_services_assign_public_ip_disabled(region=region),
        )
    )

    output = {name: result.to_dict() for name, result in results}
    print(json.dumps(output, indent=2))

    # Exit non-zero if any check failed
    any_failed = any(not r.passed for _, r in results)
    return 1 if any_failed else 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run ECS compliance checks (CIS compute controls 3.1, 3.2)"
    )
    parser.add_argument(
        "--region",
        help="AWS region to use (defaults to SDK chain)",
        default=None,
    )
    args = parser.parse_args()

    exit_code = _run_cli(region=args.region)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()


