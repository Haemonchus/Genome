# Import necessary library
import subprocess

def run_chopper(reads_path, output_path, quality_threshold, length_threshold, threads):
    """
    Automate the execution of Chopper for filtering Nanopore reads based on quality and length.

    Args:
    reads_path (str): Path to the input FASTQ file.
    output_path (str): Path to the output FASTQ file after filtering.
    quality_threshold (int): Quality threshold for filtering reads.
    length_threshold (int): Minimum length of reads to keep.
    threads (int): Number of threads to use.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    # Construct the Chopper command using redirection
    command = f"chopper -t {threads} -q {quality_threshold} -l {length_threshold} < {reads_path} > {output_path}"

    # Execute the command
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
