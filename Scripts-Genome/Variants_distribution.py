import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Set global font to Arial
rcParams['font.family'] = 'Arial'

def extract_AF_values(vcf_file):
    """
    Extract allele frequency (AF) values from a VCF file.

    Parameters:
    vcf_file (str): Path to the VCF file.

    Returns:
    list: List of AF values.
    """
    AF_list = []
    with open(vcf_file, 'r') as f:
        for line in f:
            if not line.startswith('#'):  # Skip header lines
                columns = line.strip().split('\t')
                last_column = columns[-1]
                coms = last_column.split(":")
                AO = float(coms[4])
                RO = float(coms[2])
                AF = AO / (AO + RO)
                AF_list.append(AF)
    return AF_list

# Example usage
vcf_file_1 = 'pool.vcf'
vcf_file_2 = 'single.vcf'
AF_values_pool = extract_AF_values(vcf_file_1)
AF_values_single = extract_AF_values(vcf_file_2)

def plot_histogram(data1, data2, bins=100, output_file=None):
    """
    Plot a histogram of two datasets and save the plot to a file.

    Parameters:
    data1 (list): First dataset to plot.
    data2 (list): Second dataset to plot.
    bins (int): Number of bins for the histogram. Default is 100.
    output_file (str): Path to save the plot. If None, the plot is shown instead of being saved.
    """
    plt.figure(figsize=(8, 6))  # Set the figure size
    plt.hist(data1, bins=bins, alpha=0.7, color='skyblue', label='Pool')  # Modify color and transparency
    plt.hist(data2, bins=bins, alpha=0.7, color='salmon', label='Single')  # Modify color and transparency

    # Calculate mean and median for data1 and data2
    mean_data1 = np.mean(data1)
    mean_data2 = np.mean(data2)
    median_data1 = np.median(data1)
    median_data2 = np.median(data2)

    # Display median on the plot
    plt.axvline(median_data1, color='skyblue', linestyle='-.', label=f'Median Pool: {median_data1:.2f}')
    plt.axvline(median_data2, color='salmon', linestyle='-.', label=f'Median Single: {median_data2:.2f}')

    # Set tick font sizes
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Remove top and right borders
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()  # Adjust layout

    if output_file:
        plt.savefig(output_file, dpi=800)  # Save the figure with specified resolution
    else:
        plt.show()  # Show the plot

# Generate filename for the output image
output_file = 'noX_New_100_advanced_histogram.png'

# Plot and save the histogram
plot_histogram(AF_values_pool, AF_values_single, bins=100, output_file=output_file)
