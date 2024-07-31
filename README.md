## Introduction
T2Tools is a toolset contains several tools for T2T assembly, and it is under development.

## Dependencies
### Software
* Python (>=3.7)
* [TRF](https://github.com/Benson-Genomics-Lab/TRF) (Tandem Repeat Finder)
### Python Modules
* matplotlib
* numpy
* pathos

## Usage

### 1. Identify centromere and telomere for genome
a) Usage
```bash
usage: t2tools.py centel [-h] -f FASTA [-p] [-w WINDOW_SIZE] [-s STEP_SIZE] [--lower LOWER] [--upper UPPER] [--copy COPY] [--score SCORE] -o OUTPUT [-t THREADS]

options:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        fasta file or directory
  -p, --split           split fasta or not, only for single fasta
  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        window size for splitting fasta, must be integer or scientific notation, like: 10000, 1e4
  -s STEP_SIZE, --step_size STEP_SIZE
                        step size for splitting fasta, must be integer or scientific notation, like: 10000, 1e4
  --lower LOWER         lower size of centromere repeat monomer, default=50
  --upper UPPER         upper size of centromere repeat monomer, default=200
  --copy COPY           minium copy number of centromere repeat monomer, default=10
  --score SCORE         minium score of centromere repeat monomer, default=2000
  -o OUTPUT, --output OUTPUT
                        output directory
  -t THREADS, --threads THREADS
                        threads, default: 10
```
b) Example
```shell
t2tools.py centel -f chrom_dir -o wrkdir -t 24 --lower 50 --upper 250
```

c) Result
* **trf_total.bed**: a text file that contain several columns extracted from the dat file of trf like below

| sid  | start_pos | end_pos | length | copy_num | score  | pattern | seq                         |
|------|-----------|---------|--------|----------|--------|---------|-----------------------------|
| Chr1 | 11        | 2711    | 2701   | 432.2    | 2306.0 | ACCCTA  | ACCCTAACCCTAACCCTAACCCTA... |

* **centro.list**: a text file that contain candidate centromere regions
* **telo.list**: a text file that contain candidate telomere regions
* **whole.pdf**: a distribution plot of "Repeat monomer length (nt)" and "Number of monomer"
* **separated.pdf**: similar with whole.pdf but draw each chromosome separately 