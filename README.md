# Domain Witch
A tool like `domain hunter` running over DNS, IP addresses and other stuff and making a simple quick and dirty output from it. It's purpose is to aid ease of analysis.


## Requirements
See [requirements.txt](requirements.txt) for the current dependencies.


## Preparations

### Create virtual env
```bash
python3 -m venv .venv
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Usage
```bash
python3 main.py <input file> <output file>
```

Warning: TCP checker is unstable in large list quantities!
