#!/usr/bin/env python3
import os
import subprocess
import time
import sys


def calculate_n50(contig_file):
    """Calculate N50 from a contig FASTA file"""
    lengths = []
    
    if not os.path.exists(contig_file):
        return 0
    
    with open(contig_file, 'r') as f:
        current_length = 0
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_length > 0:
                    lengths.append(current_length)
                    current_length = 0
            else:
                current_length += len(line)
        if current_length > 0:
            lengths.append(current_length)
    
    if not lengths:
        return 0
    
    # Sort lengths in descending order
    lengths.sort(reverse=True)
    
    # Calculate total length
    total_length = sum(lengths)
    half_length = total_length / 2
    
    # Find N50
    cumulative_length = 0
    for length in lengths:
        cumulative_length += length
        if cumulative_length >= half_length:
            return length
    
    return 0


def run_command(cmd, cwd):
    """Run a command and return the runtime in seconds"""
    start_time = time.time()
    try:
        # Set stack size limit
        env = os.environ.copy()
        
        # Run with increased stack size using bash
        full_cmd = f"ulimit -s 8192000 && {cmd}"
        
        # Run command and capture output (but don't print it)
        process = subprocess.Popen(
            full_cmd,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            executable='/bin/bash'
        )
        
        # Capture output but don't print it
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error: Command failed with return code {process.returncode}", file=sys.stderr)
            if stderr:
                print(f"stderr: {stderr}", file=sys.stderr)
            return None
            
    except Exception as e:
        print(f"Exception running command: {cmd}", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        return None
    
    end_time = time.time()
    return end_time - start_time


def format_time(seconds):
    """Format seconds into HH:MM:SS format"""
    if seconds is None:
        return "ERROR"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:01d}:{minutes:02d}:{secs:02d}"


def main():
    # Set up directories - use the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    code_dir = os.path.join(base_dir, "code")
    data_dir = os.path.join(base_dir, "data")
    
    # Datasets to process
    datasets = ["data1", "data2", "data3", "data4"]
    
    # Results storage
    results = []
    
    # Process each dataset
    for dataset in datasets:
        dataset_path = os.path.join(data_dir, dataset)
        
        # Check if dataset exists
        if not os.path.exists(dataset_path):
            print(f"Dataset {dataset} not found at {dataset_path}", file=sys.stderr)
            continue
        
        # First, backup any existing contig.fasta
        contig_file_path = os.path.join(dataset_path, "contig.fasta")
        python_contig_file = os.path.join(dataset_path, "contig_python.fasta")
        codon_contig_file = os.path.join(dataset_path, "contig_codon.fasta")
        
        # Run Python version
        python_cmd = f"python3 code/main.py data/{dataset}"
        python_time = run_command(python_cmd, base_dir)
        
        # Save Python results
        if os.path.exists(contig_file_path):
            subprocess.run(f"cp {contig_file_path} {python_contig_file}", shell=True)
        
        # Calculate N50 for Python results
        python_n50 = calculate_n50(python_contig_file)
        
        # Store Python results
        results.append({
            'dataset': dataset,
            'language': 'python',
            'runtime': python_time,
            'n50': python_n50
        })
        
        # Run Codon version
        # Check if codon is in PATH, otherwise use the expected GitHub Actions location
        codon_path = "codon"
        if os.environ.get('GITHUB_ACTIONS'):
            potential_codon = os.path.expanduser("~/.codon/bin/codon")
            if os.path.exists(potential_codon):
                codon_path = potential_codon
        
        codon_cmd = f"{codon_path} run -release code/main.codon data/{dataset}"
        codon_time = run_command(codon_cmd, base_dir)
        
        # Save Codon results
        if os.path.exists(contig_file_path):
            subprocess.run(f"cp {contig_file_path} {codon_contig_file}", shell=True)
        
        # Calculate N50 for Codon results
        codon_n50 = calculate_n50(codon_contig_file)
        
        # Store Codon results
        results.append({
            'dataset': dataset,
            'language': 'codon',
            'runtime': codon_time,
            'n50': codon_n50
        })
    
    # Print results table in the requested format
    print("Dataset\tLanguage\tRuntime\t\tN50")
    print("-" * 70)
    
    # Print results
    for result in results:
        runtime_str = format_time(result['runtime'])
        print(f"{result['dataset']}\t{result['language']}\t\t{runtime_str}\t\t{result['n50']}")


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    main()
