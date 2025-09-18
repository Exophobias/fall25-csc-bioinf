# LLM Usage
Model Used: `Claude Opus 4`

## Model Used
* **Model**: Claude 3.5 Sonnet (via GitHub Copilot Chat)
* **Purpose**: Assisted with Python-to-Codon conversion and evaluation script development

## Python-to-Codon Conversion
* **File Context**: Provided all 4 Python files (`main.py`, `dbg.py`, `utils.py`, `dbg_kmer_as_key.py`)
* **Initial Prompt**:
```
I was tasked with running the 4 datasets using the python script from the repository https://github.com/zhongyuchen/genome-assembly
[provided execution results]
Now I am tasked with converting main.py, utils.py, dbg.py and dbg_kmer_as_key.py to Codon and then I have to run the Codon program on data1~data4 again and compare the results.
```

* **Key Assistance Provided**:
  - Converted Python syntax to Codon syntax
  - Added explicit type annotations required by Codon
  - Identified and resolved Python-Codon compatibility issues
  - Removed Python-specific features (sys.setrecursionlimit, matplotlib import)
  - Fixed string formatting differences between Python and Codon

## Python Evaluation Script
* **File Context**: Repository structure and requirements
* **Prompt**:
```
Reading the instructor comments, we need to reproduce the NG50
The evaluate.py should do the following
We're almost there! Now write a script (say, week1/evaluate.sh; you can use any other language instead of Bash) that will:
    Run Python code automatically.
    Run Codon code automatically (use codon run -release for timing).
    Programmatically compile the results and runtimes.
[provided expected output format]
```

* **Assistance Provided**:
  - Created almost working `evaluate.py` script to automate testing
  - Implemented N50 calculation algorithm
  - Added runtime measurement and formatting
  - Handled cross-platform compatibility
  - Fixed issues with output formatting and error handling

## Debugging Assistance
* **Context**: GitHub Actions CI errors
* **Issues Resolved**:
  - Removed unnecessary matplotlib dependency
  - Fixed Codon executable path detection for CI environment
  - Made script paths relative for portability
  - Suppressed verbose output while preserving error reporting

## Key Learnings from AI Assistance
1. **Codon Differences**: The AI helped identify critical differences between Python and Codon (dictionary ordering, type requirements, string handling)
2. **Performance Benefits**: Confirmed Codon provides significant performance improvements (40-50% faster)
3. **Portability**: Emphasized importance of relative paths and environment-agnostic code
4. **Error Handling**: Improved error handling for missing dependencies and different execution environments