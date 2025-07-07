# 10 mins, 8GB
nanoQC -o Zymo_qc ../data/metagenomics/20250616_PBC42657_ZymoGutCommDNA_dorado-0.9.1.duplex_sup.fastq.gz

# 1.5 mins, 10GB
../kraken2/scripts/k2 classify --db k2_db --threads 8 --output k2.out --use-names --report k2.report ../data/metagenomics/20250616_PBC42657_ZymoGutCommDNA_dorado-0.9.1.duplex_sup.fastq.gz
