# Import necessary library
import subprocess


# Define a function to run Canu for genome assembly
def run_canu(output_dir, prefix, genome_size, raw_data_path):
    """
    Run Canu for genome assembly from Nanopore reads.

    Args:
    output_dir (str): Directory to place the Canu output files.
    prefix (str): Prefix for the output files.
    genome_size (str): Estimated size of the genome (e.g., '350m').
    raw_data_path (str): Path to the raw FASTQ file from Nanopore.

    Returns:
    str: Output from the Canu execution.
    """
    # Build the Canu command
    command = [
        'canu',
        '-d', output_dir,
        '-p', prefix,
        'genomeSize=' + genome_size,
        '-nanopore-raw', raw_data_path
    ]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
