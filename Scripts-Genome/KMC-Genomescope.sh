#!/bin/bash

# Create a temporary directory for intermediate files
mkdir tmp

# Uncomment the next line if you want to dynamically generate the FILES list from .fastq files in the current directory
# ls *.fastq > FILES

# List of k-values to iterate over
k_values=(17 19 21 23)

# List of p-values to iterate over
p_values=(1 2 3 4)

# Loop over each k-value
for k in "${k_values[@]}"
do
  # Run the KMC command with the specified k-value
  kmc -k$k -t64 -m128 -ci1 -cs10000 @FILES reads_$k tmp/

  # Transform the KMC output to a histogram using kmc_tools
  kmc_tools transform reads_$k histogram reads.histo_$k -cx10000

  # Create a directory for the current k-value results
  mkdir genomescope_k-$k

  # Loop over each p-value
  for p in "${p_values[@]}"
  do
    # Define the output folder and output name for the current k and p values
    output_folder="genomescope_k-$k/genomescope_p-$p"
    output_name="k-$k-p-$p"

    # Create the output directory
    mkdir "$output_folder"

    # Run the GenomeScope analysis with the specified parameters
    genomescope.R -i reads.histo_$k -o "$output_folder" -k $k -p $p -n "$output_name"
  done
done
