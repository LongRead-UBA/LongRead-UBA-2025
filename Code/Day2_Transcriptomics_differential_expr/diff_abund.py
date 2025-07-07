import argparse
from pydeseq2.dds import DeseqDataSet
from pydeseq2.default_inference import DefaultInference
from pydeseq2.ds import DeseqStats
from pydeseq2.utils import load_example_data
from pandas import DataFrame

parser = argparse.ArgumentParser("Differential expression using pyDESeq2")
parser.add_argument("metadata", help="TSV containing file names and classes")
args = parser.parse_args()

samples = []
for line in open(args.metadata):
    if len(line) <= 1:
        continue
    fields = line.strip().split('\t')
    if fields[0] == "filename":
        header = fields
    else:
        samples.append({header[i]:fields[i] for i in range(len(header))})

for s in samples:
    expr = {}
    for line in open(s["filename"]):
        if len(line) <= 1:
            continue
        fields = line.strip().split()
        if fields[0] == "transcript":
            header = fields
        else:
            expr[fields[header.index("transcript")]] = int(round(float(fields[header.index("reads")])))
    s["expr"] = expr

transcripts = list(set(a for s in samples for a in s["expr"]))
print(f"{len(transcripts)} unique transcripts")

counts_df = DataFrame([[s["expr"].get(t, 0) for t in transcripts] for s in samples], index=[s["filename"] for s in samples], columns=transcripts)

metadata = DataFrame([[s["lineage"], s["subtype"]] for s in samples], index=[s["filename"] for s in samples], columns=["condition", "group"])

print(counts_df)
print(metadata)

samples_to_keep = ~metadata.condition.isna()
counts_df = counts_df.loc[samples_to_keep]
metadata = metadata.loc[samples_to_keep]

genes_to_keep = counts_df.columns[counts_df.sum(axis=0) >= 10]
counts_df = counts_df[genes_to_keep]

inference = DefaultInference(n_cpus=8)
dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design="~condition",
    refit_cooks=True,
    inference=inference,
)

dds.deseq2()

print(dds)
print(dds.varm["dispersions"])
print(dds.varm["LFC"])

ds = DeseqStats(dds, contrast=["condition", "B-ALL", "AML"], inference=inference)

ds.summary()

ds.lfc_shrink(coeff="condition[T.B-ALL]")

sig = ds.results_df[ds.results_df["padj"]<0.05]
sig = sig.sort_values("padj")

print(sig)
