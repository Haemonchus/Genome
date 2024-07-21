# Import necessary library
import subprocess

def run_braker3(singularity_image, genome_path, bam_files, threads, species):
    """
    Automate the execution of Braker3 via Singularity for gene prediction.

    Args:
    singularity_image (str): Path to the Singularity image file for Braker3.
    genome_path (str): Path to the genome file.
    bam_files (list): List of BAM file paths for RNA-seq alignments.
    threads (int): Number of threads to use.
    species (str): Species name for Braker3 configuration.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    bam_list = ",".join(bam_files)  # Join all BAM paths with a comma

    # Construct the Braker3 command using Singularity
    command = [
        'singularity', 'exec', singularity_image,
        'braker.pl',
        '--genome=' + genome_path,
        '--bam=' + bam_list,
        '--threads', str(threads),
        '--species=' + species
    ]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
