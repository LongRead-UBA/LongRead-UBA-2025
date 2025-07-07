mkdir -p data
cd data

# kraken2 db:
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_08gb_20250402.tar.gz

# reference human genome:
wget https://hgdownload.soe.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz

# Ensembl transcriptome reference:
wget https://ftp.ensembl.org/pub/release-114/fasta/homo_sapiens/cdna/Homo_sapiens.GRCh38.cdna.all.fa.gz
wget https://ftp.ensembl.org/pub/release-114/gtf/homo_sapiens/Homo_sapiens.GRCh38.114.gtf.gz
