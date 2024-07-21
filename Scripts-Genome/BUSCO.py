# Import necessary library
import subprocess

def run_busco(assembly_path, lineage, output_name, mode, cpu):
    """
    Automate the execution of BUSCO for assessing the quality of genome assemblies and annotations.

    Args:
    assembly_path (str): Path to the genome assembly FASTA file.
    lineage (str): The lineage dataset to use for the BUSCO assessment.
    output_name (str): Name for the output files and directory.
    mode (str): Mode in which to run BUSCO (e.g., 'genome', 'proteins', 'transcriptome').
    cpu (int): Number of CPUs to use for the analysis.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    # Construct the BUSCO command
    command = [
        'busco',
        '-i', assembly_path,
        '-l', lineage,
        '-o', output_name,
        '-m', mode,
        '--cpu', str(cpu)
    ]

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
