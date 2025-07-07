# ~15 min, 4GB
mkdir -p RNA
for f in ../data/RNA/*.fastq.gz; do
  fn=${f##*/}
  prefix=${fn%%.fastq.gz}
  echo
  echo $prefix
  ../minimap2-2.29_x64-linux/minimap2 -t8 -cx map-ont ../data/RNA/Homo_sapiens.GRCh38.cdna.all.fa.gz $f > RNA/$prefix.paf
  ../minnow/minnow -r ../data/RNA/Homo_sapiens.GRCh38.cdna.all.fa.gz -p RNA/$prefix.paf -t 8 > RNA/$prefix.minnow.cts
done

# Differential abundance (pyDESeq2)
python diff_abund.py ../data/RNA/metadata.tsv
