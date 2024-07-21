# Import necessary library
import subprocess

def run_nanoplot(fastq_path, output_dir, threads):
    """
    Automate the execution of NanoPlot for quality control of Nanopore reads.

    Args:
    fastq_path (str): Path to the FASTQ file.
    output_dir (str): Output directory for NanoPlot results.
    threads (int): Number of threads to use.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    # Construct the NanoPlot command
    command = [
        'NanoPlot',
        '-t', str(threads),
        '-o', output_dir,
        '--fastq', fastq_path
    ]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")

