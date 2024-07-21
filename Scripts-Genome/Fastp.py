# Import necessary libraries
import argparse
import subprocess


# Define a function to run fastp
def run_fastp(input_file, output_file, report_file, extra_args=[]):
    """
    Run fastp for quality control of reads.

    Args:
    input_file (str): Path to the input FASTQ file.
    output_file (str): Path to the output FASTQ file.
    report_file (str): Path to the output JSON report file.
    extra_args (list): List of additional arguments to pass to fastp.

    Returns:
    str: Output from the fastp execution.
    """
    # Build the basic fastp command
    command = [
                  'fastp',
                  '-i', input_file,
                  '-o', output_file,
                  '-j', report_file,
                  '-h', output_file.replace('.fastq', '.html')
              ] + extra_args

    # Execute the command
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


# Set up command line argument parsing
def main():
    parser = argparse.ArgumentParser(description="Quality control for FASTQ files using fastp.")
    parser.add_argument("input_file", type=str, help="Input FASTQ file path")
    parser.add_argument("output_file", type=str, help="Output FASTQ file path")
    parser.add_argument("report_file", type=str, help="JSON report file path")
    parser.add_argument("--extra_args", nargs='*', help="Extra arguments for fastp", default=[])

    args = parser.parse_args()

    # Execute fastp
    output = run_fastp(args.input_file, args.output_file, args.report_file, args.extra_args)
    print(output)


