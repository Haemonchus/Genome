import subprocess

def run_freebayes(reference_path, bam_path, output_vcf_path, extra_args=None):
    """
    Automate the execution of freebayes for variant calling.

    Args:
    reference_path (str): Path to the reference genome FASTA file.
    bam_path (str): Path to the input BAM file with alignments.
    output_vcf_path (str): Path where the output VCF file will be saved.
    extra_args (list of str, optional): A list of additional arguments as strings to pass to freebayes.
    """
    # Basic freebayes command
    command = ['freebayes', '-f', reference_path, bam_path]

    # If there are extra arguments, extend the command list with them
    if extra_args:
        command.extend(extra_args)

    # Redirecting the output to the VCF file
    with open(output_vcf_path, 'w') as output_file:
        try:
            # Executing the command and writing output to VCF file
            subprocess.run(command, stdout=output_file, check=True)
            print(f"Variant calling complete. VCF saved to {output_vcf_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error running freebayes: {e}")

