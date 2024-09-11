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


## Installation

Add <kbd>TRF</kbd> to your environment variable PATH
```bash
cd /path/to/install
git clone https://github.com/sc-zhang/T2Tools.git
pip install -r requirements.txt
chmod +x T2Tools/t2tools.py
echo 'export PATH=/path/to/install/T2Tools:$PATH' >> ~/.bash_profile
source ~/.bash_profile
```


## Usage

### 0. Main program
```bash
usage: t2tools.py [-h] {centel,gap} ...

options:
  -h, --help    show this help message and exit

sub commands:
  {centel,gap}
    centel      Identify centromeres and telomeres
    gapcount    Get gap counts
```
> **Notice:** details of sub commands were described below.


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


### 2. Get gap counts
a) Usage
```bash
usage: t2tools.py gapcount [-h] -f FASTA [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        fasta file
  -o OUTPUT, --output OUTPUT
                        output statistic, if not set, output to stdout
```

b) Example
```bash
t2tools.py gapcount -f chrom.fa -o chrom.gap_cnt.txt
```

c) Result
A text file with two columns, first column is sequence id, second column is gap count, 
the last row is "Total" means total count of gaps  
