# Set the working directory
setwd("path_to_your_dir")

# Load necessary libraries
library(clusterProfiler)
library(dplyr)
library(stringr)
library(enrichplot)

# Prepare the list of genes to be enriched
# Note: Update the file name if working with a different dataset
data <- read.table("your_file", header = FALSE)
genes <- as.character(data$V1)  # Convert to character format

# Read the EggNOG annotation file
# Note: The EggNOG file should have all '#' symbols removed
egg <- read.csv("your_anno.tsv", header = TRUE, sep = "\t")
# If read.csv gives an error, try using read.table or rio::import

# Replace empty strings with NA
egg[egg == ""] <- NA

# Display the column names for reference
# This is useful for identifying the columns needed for GO, KEGG, and other enrichment analyses
colnames(egg)

# Extract KO terms from the EggNOG results
koterms <- egg %>%
  dplyr::select(GID = query, KO = KEGG_ko) %>%
  na.omit() %>%
  filter(str_detect(KO, "ko"))

# Preview the first six rows of koterms
head(koterms)

# Download KO to pathway mapping from KEGG:
# https://www.genome.jp/kegg-bin/get_htext?ko00001 (Click Download JSON)
# Place the JSON file in the working directory, then run KEGG_frined.R to generate kegg_info.RData

# Load the KEGG information
load("kegg_info.RData")  # This will load ko2pathway and pathway2name objects

# Rename columns in ko2pathway to match koterms
colnames(ko2pathway) = c("KO", "Pathway")

# Remove 'ko:' prefix from KO terms in koterms
koterms$KO = str_replace_all(koterms$KO, "ko:", "")

# Merge koterms with ko2pathway to get gene-to-pathway mapping
gene2pathway <- koterms %>%
  left_join(ko2pathway, by = "KO") %>%
  dplyr::select(GID, Pathway) %>%
  na.omit()

# Create a combined table with pathway names (optional)
gene2pathway_name <- left_join(gene2pathway, pathway2name, by = "Pathway")
# Save the combined table to a file (optional)
write.table(gene2pathway_name, file = "gene2pathway_name.txt", sep = "\t", row.names = FALSE, quote = FALSE)

# Adjust the order and format for enrichment analysis
p2gene <- gene2pathway_name[, c(2, 1)]
p2name <- gene2pathway_name[, c(2, 3)]

# Perform enrichment analysis using the 'enricher' function
ego <- enricher(genes, TERM2GENE = p2gene, TERM2NAME = p2name, pAdjustMethod = "BH")

# Visualize the enrichment results
dotplot(ego)
barplot(ego, showCategory = 20)
print(ego)

# Optional: Add qscore for visualization and plot
mutate(ego, qscore = -log(p.adjust, base = 30)) %>%
  barplot(x = "Count")

# Dotplots with titles for ORA and GSEA
dotplot(ego, showCategory = 30) + ggtitle("Dotplot for ORA")
dotplot(ego, showCategory = 30) + ggtitle("Dotplot for GSEA")

# Save the enrichment results to a file
write.table(as.data.frame(ego), "1574_pathway_enrich.csv", sep = "\t", row.names = FALSE, quote = FALSE)
