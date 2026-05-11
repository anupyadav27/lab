import requests
from bs4 import BeautifulSoup
import csv
import re
import time

AWS_SERVICES = ["account", "acm", "amplify", "apigateway", "appflow", "apprunner", "appstream", "athena", "autoscaling", "backup", "cloudformation", "cloudfront", "cloudtrail", "cloudwatch", "codebuild", "codepipeline", "config", "documentdb", "dynamodb", "ec2", "ecr", "ecs", "efs", "eks", "elasticache", "elasticbeanstalk", "elasticsearch", "elb", "emr", "eventbridge", "fsx", "glue", "guardduty", "iam", "kinesis", "kms", "lambda", "logs", "msk", "neptune", "opensearch", "rds", "redshift", "route53", "s3", "sagemaker", "secretsmanager", "securityhub", "sns", "sqs", "ssm", "stepfunctions", "waf"]

BASE_URL = "https://docs.aws.amazon.com/securityhub/latest/userguide/"

def scrape_service_controls(service_name):
    url = f"{BASE_URL}{service_name}-controls.html"
    try:
        print(f"Scraping {service_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        controls = []
        control_sections = soup.find_all(['h2', 'h3'], string=re.compile(r'\[.*\.\d+\]'))
        for section in control_sections:
            control_data = extract_control_data(section, soup, service_name, url)
            if control_data:
                controls.append(control_data)
        print(f"  Found {len(controls)} controls")
        return controls
    except Exception as e:
        print(f"  Error: {e}")
        return []

def extract_control_data(section, soup, service_name, base_url):
    try:
        section_title = section.get_text().strip()
        control_id_match = re.search(r'\[(.*?\.\d+)\]\s*(.*)', section_title)
        if not control_id_match:
            return None
        control_id = control_id_match.group(1)
        title = control_id_match.group(2).strip()
        control_info = {'Title': title, 'RelatedRequirements': '', 'Category': '', 'Severity': '', 'ResourceType': '', 'ConfigRule': ''}
        current = section.find_next_sibling()
        while current and not (current.name in ['h2', 'h3'] and re.search(r'\[.*\.\d+\]', current.get_text())):
            text = current.get_text().strip()
            if text.startswith('Related requirements:') or text.startswith('Related requirement:'):
                control_info['RelatedRequirements'] = re.sub(r'^Related requirements?:\s*', '', text)
            elif text.startswith('Category:'):
                control_info['Category'] = re.sub(r'^Category:\s*', '', text)
            elif text.startswith('Severity:'):
                control_info['Severity'] = re.sub(r'^Severity:\s*', '', text)
            elif text.startswith('Resource type:'):
                control_info['ResourceType'] = re.sub(r'^Resource type:\s*', '', text)
            elif text.startswith('AWS Config rule:'):
                control_info['ConfigRule'] = re.sub(r'^AWS Config rule:\s*', '', text)
            current = current.find_next_sibling()
            if current is None:
                break
        anchor = f"{service_name}-{control_id.split('.')[1]}"
        link = f"{base_url}#{anchor}"
        return {'Control ID': control_id, 'Title': control_info['Title'], 'Severity': control_info['Severity'], 'Resource Type': control_info['ResourceType'], 'Related Requirements': control_info['RelatedRequirements'], 'Category': control_info['Category'], 'AWS Config Rule': control_info['ConfigRule'], 'Link': link}
    except Exception as e:
        print(f"    Error extracting {section_title}: {e}")
        return None

def main():
    print("Starting AWS Security Hub Controls Scraper")
    print("=" * 60)
    all_controls = []
    for service in AWS_SERVICES:
        controls = scrape_service_controls(service)
        all_controls.extend(controls)
        time.sleep(0.5)
    output_file = 'aws_security_hub_controls_final.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Control ID', 'Title', 'Severity', 'Resource Type', 'Related Requirements', 'Category', 'AWS Config Rule', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_controls)
    print("=" * 60)
    print(f"✓ Successfully scraped {len(all_controls)} controls")
    print(f"✓ Saved to {output_file}")

if __name__ == '__main__':
    main()
