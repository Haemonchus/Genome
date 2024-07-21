# Import necessary library
import subprocess

def run_quast_simple(assembly_path, output_dir):
    """
    Automate the execution of QUAST for quality assessment of genome assemblies with minimal arguments.

    Args:
    assembly_path (str): Path to the genome assembly FASTA file.
    output_dir (str): Directory where QUAST results will be saved.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    # Construct the QUAST command
    command = [
        'quast.py',
        assembly_path,
        '-o', output_dir
    ]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
