# dynamic_resume
Creates a resume based on a yaml file. Ideal for incorporation with ChatGPT to quickly iterate over various resumes accounting for job description and other context.

## Installation

Use the package manager git clone https://github.com/Jtth3brick/dynamic_resume.git

## Prerequisites

Before using this Git repository, you must have the following packages installed:

 - yaml
 - argparse
 - fpdf

To install these packages, you can use pip, a package manager for Python. Simply run the following commands in your terminal:

```
pip install pyyaml
pip install argparse
pip install fpdf
```

Note: This Git repository requires Python 3.x to be installed on your system. If you haven't installed it yet, please visit the official Python website and follow the installation instructions for your platform.

## Usage

First fill out resume.yaml

Run

```
python3 compile.py --size 0.95
```

A compiled pdf should appear in the directory

## TODO

Finish resume.py
 - Automatically find a text size to fit all data in one page

crawler.py
 - take website url as input and put all text data with custom depth into single output for gpt context
