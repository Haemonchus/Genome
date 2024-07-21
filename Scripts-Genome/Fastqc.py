# Import necessary library
import subprocess

def run_fastqc(r1_fastq, r2_fastq, output_dir, threads):
    """
    Automate the execution of FastQC for quality control of sequencing reads.

    Args:
    r1_fastq (str): Path to the R1 FASTQ file.
    r2_fastq (str): Path to the R2 FASTQ file.
    output_dir (str): Directory where FastQC results will be saved.
    threads (int): Number of threads to use.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    # Construct the FastQC command
    command = [
        'fastqc',
        '-t', str(threads),
        '-o', output_dir,
        r1_fastq,
        r2_fastq
    ]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
