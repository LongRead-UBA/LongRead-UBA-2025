if [ ! -s ../data/hg38.fa ]; then
  gunzip ../data/DNA/hg38.fa.gz
fi
if [ ! -s ../data/DNA/hg38.fa.fai ]; then
  samtools faidx ../data/DNA/hg38.fa
fi

# 7.5 mins, 2.3 GB
nanoQC -o SKES1_qc ../data/DNA/20250522_PBE28753_SKES1_WGS_DNA.chr11_22.fastq.gz

# ~600s, 20GB
../minimap2-2.29_x64-linux/minimap2 -t8 -ax lr:hq ../data/DNA/hg38.fa ../data/DNA/20250522_PBE28753_SKES1_WGS_DNA.chr11_22.fastq.gz > SKES1_hg38.sam

# ~5 min
samtools view -bS SKES1_hg38.sam | samtools sort -t8 -o SKES1_hg38.sorted.bam
samtools index SKES1_hg38.sorted.bam

# 44s, 1.1GB
sniffles --input SKES1_hg38.sorted.bam --vcf SKES1_sniffles.vcf --threads 8

# 21m, 2GB
conda init
source ~/.bashrc
conda activate clair3
../Clair3/run_clair3.sh --bam_fn=SKES1_hg38.sorted.bam --ref_fn=../data/DNA/hg38.fa --threads=8 --platform=ont --model_path=../Clair3/models/r1041_e82_400bps_hac_v500 --output=SKES1_clair3
