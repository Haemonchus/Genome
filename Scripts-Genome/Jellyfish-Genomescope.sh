#!/bin/bash

# Directory containing the input FASTQ files
fastq_dir="path_to_your_dir"

# List of k-values to iterate over
k_values=(17 19 21 23)

# List of p-values to iterate over
p_values=(1 2 3 4)

# Loop over each k-value
for k in "${k_values[@]}"
do
  # Run the Jellyfish count command with the specified k-value
  jellyfish count -C -m $k -s 1000000000 -t 10 "$fastq_dir"/*.fastq -o reads_$k.jf

  # Generate a histogram from the Jellyfish output
  jellyfish histo -t 64 reads_$k.jf > reads_$k.histo

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
    genomescope.R -i reads_$k.histo -o "$output_folder" -k $k -p $p -n "$output_name"
  done
done
