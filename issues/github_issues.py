"""
Fill up the following information before running this script.
"""
import csv

import requests as requests

GITHUB_TOKEN = ""
REPO_OWNER = "tenable"
REPO_NAME = "pyTenable"


def get_issues():
    get_issues_endpoint = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    get_issues_headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}"
    }
    get_issues_params = {
        "per_page": 100
    }
    issues = requests.get(get_issues_endpoint, params=get_issues_params, headers=get_issues_headers)
    if issues.status_code == 200:
        response = issues.json()
        get_issue_specifics(response)


def get_issue_specifics(response):
    # For each element in response,
    #   if it is not a pull request,
    #       create a dictionary with only the select elements, and add them to the list - issues.
    issues = [{
        "url": issue["html_url"],
        "issue_number": issue["number"],
        "state_of_issue": issue["state"],
        "title": issue["title"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"]
    } for issue in response if "pull_request" not in issue]
    write_to_csv(issues)


def write_to_csv(issues):
    keys = issues[0].keys()
    with open('issues.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, keys)
        writer.writeheader()
        writer.writerows(issues)


if __name__ == '__main__':
    get_issues()
