# Import necessary library
import subprocess

def run_purge_haplotigs(lib_pattern, draft_genome, pe_reads, ont_reads1, ont_reads2, threads):
    """
    Automate the process of removing haplotigs using purge_haplotigs pipeline.

    Args:
    lib_pattern (str): Pattern to match PE read files.
    draft_genome (str): Path to the draft genome FASTA file.
    pe_reads (str): Path to the paired-end reads.
    ont_reads1 (str): Path to the first Oxford Nanopore reads.
    ont_reads2 (str): Path to the second Oxford Nanopore reads.
    threads (int): Number of threads to use for processes.

    Returns:
    None: This function prints outputs directly and manages files without returning.
    """
    # Constructing and executing commands
    commands = [
        f"conda activate haplotig",
        f"bwa index {draft_genome}",
        f"bwa mem -t {threads} {draft_genome} {pe_reads} | samtools sort -@{threads} -o 500.bam -",
        "samtools index 500.bam",
        f"minimap2 -t {threads} -ax map-ont {draft_genome} {ont_reads1} {ont_reads2} --secondary=no | samtools sort -m 100G -o LR.bam -T tmp2.ali",
        "samtools index LR.bam",
        "samtools merge haecon5.bam 500.bam LR.bam",
        f"purge_haplotigs hist -b haecon5.bam -g {draft_genome} -t {threads}",
        "rm 500.bam LR.bam",
        "purge_haplotigs cov -i haecon5.bam.gencov -l 1 -m 85 -h 175 -o coverage_stats.csv",
        f"purge_haplotigs purge -g {draft_genome} -c coverage_stats.csv -t {threads}",
        "conda deactivate"
    ]

    # Execute each command in the sequence
    for command in commands:
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Command: {command}\nOutput: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error in command: {command}\nError: {e.stderr}")
