## Introduction
T2Tools is a tool contains several tools for T2T assembly, and it is under development.

## Dependencies
### Software
* Python 3
* TRF (Tandem Repeat Finder)
### Python Modules
* pathos

## Usage

1. Identify centromere and telomere for genome
```bash
usage: T2Tools.py centrotelo [-h] -f FASTA [-p] [-w WINDOW_SIZE] [-s STEP_SIZE] -o OUTPUT [-t THREADS]

options:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        fasta file or directory
  -p, --split           split fasta or not, only for single fasta
  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        window size for splitting fasta, must be integer or scientific notation, like: 10000, 1e4
  -s STEP_SIZE, --step_size STEP_SIZE
                        step size for splitting fasta, must be integer or scientific notation, like: 10000, 1e4
  -o OUTPUT, --output OUTPUT
                        output directory
  -t THREADS, --threads THREADS
                        threads, default: 10

```
