# Deliverable 1

## Summary
This project converted a Python-based genome assembler to Codon and evaluated both implementations on 4 datasets. While both versions successfully assembled genomes and calculated N50 values, **the original repository is not reproducible as-is**. 

The calculated N50 values differ from those reported in the original repository's table:
- **data1**: Our N50: 9990 vs Original: 9118.8
- **data2**: Our N50: 9992 vs Original: 9129.2  
- **data3**: Our N50: 9824 vs Original: 7859.2
- **data4**: Our N50: 159255 vs Original: 55757.8

These discrepancies likely stem from:
1. The original results table showing NGA50 (which requires a reference genome) rather than N50
2. Missing reference genomes needed to reproduce the exact metrics
3. Possible differences in post-processing or filtering steps not included in the public repository

Despite these differences, the Codon conversion was successful, producing identical N50 values to the Python version while achieving 40-50% performance improvements.


## Repository Setup
Model Used: `Claude Opus 4`
---
The repository structure follows the required format:
```
week1/
├── code/           # Contains both Python and Codon implementations
│   ├── main.py
│   ├── dbg.py
│   ├── utils.py
│   ├── dbg_kmer_as_key.py
│   ├── main.codon
│   ├── dbg.codon
│   ├── utils.codon
│   └── dbg_kmer_as_key.codon
├── data/           # Contains the 4 datasets
│   ├── data1/
│   ├── data2/
│   ├── data3/
│   └── data4/
├── evaluate.py     # Evaluation script
├── report.md       # This report
└── ai.md          # AI usage documentation
```

GitHub Actions CI is configured to automatically run the evaluation script on push.

## Python Setup & Runs
Model Used: `Claude Opus 4`
---
The original Python implementation from https://github.com/zhongyuchen/genome-assembly was set up and tested with all 4 datasets. The code implements a de Bruijn graph-based genome assembler.

### Python Results:
- **data1**: 20 contigs, largest: 15650bp, N50: 9990bp
- **data2**: 20 contigs, largest: 15744bp, N50: 9992bp  
- **data3**: 20 contigs, largest: 9824bp, N50: 9824bp
- **data4**: 20 contigs, largest: 173867bp, N50: 159255bp

## Codon Conversion & Runs
Model Used: `Claude Opus 4` 
---

### Codon Conversion
Using Claude 3.5 Sonnet, I converted the Python files to Codon. Key changes required:

1. **Type Annotations**: Added explicit type annotations for all variables and function parameters
2. **String Operations**: Replaced Python's `%` formatting with string concatenation
3. **Removed Python Interop**: Eliminated `sys.setrecursionlimit()` as Codon handles recursion differently
4. **Dictionary Ordering**: Accounted for Codon's dictionaries not preserving insertion order
5. **Import Adjustments**: Removed unnecessary imports (matplotlib) that were causing issues

### Codon Runs
The Codon implementation produces nearly identical results to Python:
- Same N50 values for all datasets
- Minor variations in some contig lengths due to dictionary ordering differences
- **Performance improvement**: Codon runs 40-50% faster than Python

## Evaluation Script
---
The `evaluate.py` script automates running both implementations and comparing results.

### Features:
- Automatically runs Python and Codon versions on all datasets
- Calculates N50 values from assembled contigs
- Measures and reports runtime for each execution
- Outputs results in a clean table format
- Handles errors gracefully (e.g., missing Codon installation)

### Run 1
```
ryan@Ryan-Desktop:~/fall25-csc-bioinf/week1$ cd /home/ryan/fall25-csc-bioinf/week1 && python3 evaluate.py 2>&1 | tail -20
Dataset Language        Runtime         N50
----------------------------------------------------------------------
data1   python          0:00:11         9990
data1   codon           0:00:06         9990
data2   python          0:00:23         9992
data2   codon           0:00:12         9992
data3   python          0:00:26         9824
data3   codon           0:00:13         9824
data4   python          0:04:28         159255
data4   codon           0:02:40         159255
```

### Run 2
```
ryan@Ryan-Desktop:~/fall25-csc-bioinf/week1$ cd /home/ryan/fall25-csc-bioinf/week1 && python3 evaluate.py 2>&1 | head -10
Dataset Language        Runtime         N50
----------------------------------------------------------------------
data1   python          0:00:12         9990
data1   codon           0:00:06         9990
data2   python          0:00:23         9992
data2   codon           0:00:12         9992
data3   python          0:00:27         9824
data3   codon           0:00:13         9824
data4   python          0:04:29         159255
data4   codon           0:02:41         159255
```

### Hiccups
1. **Matplotlib Import**: The original code imported matplotlib which wasn't necessary for the core functionality. Had to remove this import.
2. **Codon Path in CI**: GitHub Actions required special handling to find the Codon executable.
3. **Dictionary Ordering**: Codon's dictionaries don't preserve insertion order, leading to minor differences in contig ordering.