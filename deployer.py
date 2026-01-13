#!/usr/bin/env python3
"""Turner Works Mermaid Diagram Deployer

Automatically scan GitHub repositories and add Mermaid architecture diagrams
to those that don't have them.
"""

import os
import re
import argparse
import requests
from typing import Optional

# Turner Works Branding Colors
COLORS = {
    'core': '#40C4D4',      # Turquoise - Core systems
    'user': '#4CAF50',      # Green - User interactions
    'external': '#FFF9C4',  # Yellow - External services
    'dataflow': '#2196F3',  # Blue - Data flow
}

class MermaidDeployer:
    def __init__(self, token: str, org: str):
        self.token = token
        self.org = org
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def get_repos(self) -> list:
        """Get all repositories in the organization."""
        repos = []
        page = 1
        while True:
            url = f'{self.base_url}/orgs/{self.org}/repos?page={page}&per_page=100'
            resp = requests.get(url, headers=self.headers)
            if resp.status_code != 200:
                # Try user repos if org fails
                url = f'{self.base_url}/users/{self.org}/repos?page={page}&per_page=100'
                resp = requests.get(url, headers=self.headers)
            data = resp.json()
            if not data:
                break
            repos.extend(data)
            page += 1
        return repos
    
    def has_mermaid_diagram(self, repo_name: str) -> bool:
        """Check if README contains a Mermaid diagram."""
        url = f'{self.base_url}/repos/{self.org}/{repo_name}/readme'
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return False
        
        import base64
        content = base64.b64decode(resp.json().get('content', '')).decode('utf-8')
        mermaid_patterns = ['```mermaid', 'flowchart', 'graph TD', 'graph LR', 'sequenceDiagram']
        return any(pattern in content for pattern in mermaid_patterns)
    
    def generate_diagram(self, repo_name: str) -> str:
        """Generate a Turner Works branded Mermaid diagram."""
        return f'''```mermaid
flowchart TD
    subgraph Core["{repo_name} Core"]
        style Core fill:{COLORS['core']},stroke:#333,stroke-width:2px
        A[Main Module]
        B[Processing]
    end
    
    subgraph Users["User Interface"]
        style Users fill:{COLORS['user']},stroke:#333,stroke-width:2px
        C[Input Handler]
    end
    
    subgraph External["External Services"]
        style External fill:{COLORS['external']},stroke:#333,stroke-width:2px
        D[API Integration]
    end
    
    C -->|requests| A
    A -->|processes| B
    B -->|calls| D
    
    linkStyle default stroke:{COLORS['dataflow']},stroke-width:2px
```'''
    
    def create_branch(self, repo_name: str) -> str:
        """Create a new branch for the diagram addition."""
        branch_name = f'mermaid/add-diagram-{repo_name}'
        
        # Get default branch SHA
        url = f'{self.base_url}/repos/{self.org}/{repo_name}/git/refs/heads/main'
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            url = f'{self.base_url}/repos/{self.org}/{repo_name}/git/refs/heads/master'
            resp = requests.get(url, headers=self.headers)
        
        sha = resp.json().get('object', {}).get('sha')
        
        # Create new branch
        url = f'{self.base_url}/repos/{self.org}/{repo_name}/git/refs'
        data = {'ref': f'refs/heads/{branch_name}', 'sha': sha}
        requests.post(url, headers=self.headers, json=data)
        
        return branch_name
    
    def run(self, dry_run: bool = False):
        """Run the deployer on all repos."""
        repos = self.get_repos()
        print(f'Found {len(repos)} repositories')
        
        for repo in repos:
            name = repo['name']
            if self.has_mermaid_diagram(name):
                print(f'[SKIP] {name} - already has Mermaid diagram')
                continue
            
            print(f'[ADD] {name} - needs Mermaid diagram')
            if not dry_run:
                diagram = self.generate_diagram(name)
                print(f'  Generated diagram for {name}')
                # Branch creation and PR logic would go here

def main():
    parser = argparse.ArgumentParser(description='Turner Works Mermaid Deployer')
    parser.add_argument('--org', required=True, help='GitHub organization or user')
    parser.add_argument('--dry-run', action='store_true', help='List repos without making changes')
    args = parser.parse_args()
    
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print('Error: GITHUB_TOKEN environment variable required')
        return 1
    
    deployer = MermaidDeployer(token, args.org)
    deployer.run(dry_run=args.dry_run)
    return 0

if __name__ == '__main__':
    exit(main())
