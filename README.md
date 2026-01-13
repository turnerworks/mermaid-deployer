# Turner Works Mermaid Deployer

Automatically add Turner Works branded Mermaid architecture diagrams to your GitHub repositories.

## Features

- Scans all repositories in an organization for missing Mermaid diagrams
- Generates branded architecture diagrams with Turner Works color scheme
- Creates pull requests with diagrams added to README.md or docs/architecture.md
- Supports batch processing across multiple repos

## Turner Works Branding Colors

| Element | Color | Hex |
|---------|-------|-----|
| Core Systems | Turquoise | #40C4D4 |
| User Interactions | Green | #4CAF50 |
| External Services | Yellow | #FFF9C4 |
| Data Flow | Blue | #2196F3 |

## Usage

```bash
python deployer.py --org turnerworks
```

## How It Works

1. Scans each repo's README for existing Mermaid diagrams
2. If no diagram found, generates one based on repo structure
3. Creates branch `mermaid/add-diagram-<repo>`
4. Opens PR with title "Add Turner Works system architecture diagram"

## Requirements

- Python 3.8+
- GitHub Personal Access Token with repo access
- `requests` library

## Installation

```bash
pip install -r requirements.txt
export GITHUB_TOKEN=your_token_here
python deployer.py --org turnerworks
```

## License

MIT License - see LICENSE file
