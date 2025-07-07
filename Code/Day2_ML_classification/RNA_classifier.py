import argparse
from sklearn.ensemble import RandomForestClassifier
#from sklearn.neural_network import MLPClassifier
#from sklearn.linear_model import SGDClassifier
#from sklearn import svm

parser = argparse.ArgumentParser("Train and classify by expression profile")
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
            expr[fields[header.index("transcript")]] = float(fields[header.index("TPM")])
    s["expr"] = expr

transcripts = list(set(a for s in samples for a in s["expr"]))
print(f"{len(transcripts)} unique transcripts")

for test_idx in range(len(samples)):
    train_idx = [i for i in range(len(samples)) if i != test_idx]
    train_data = [[samples[s]["expr"].get(t, 0) for t in transcripts] for s in train_idx]
    train_lineage = [samples[s]["lineage"] for s in train_idx]
    train_subtype = [samples[s]["subtype"] for s in train_idx]

    test_data = [[samples[test_idx]["expr"].get(t, 0) for t in transcripts]]

    rfc = RandomForestClassifier(max_depth=2, random_state=0) # perfect at lineage, crap at subtype
    #rfc = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,2), random_state=1) # SLOW and bad at both
    #rfc = SGDClassifier(loss="hinge", penalty="l2", max_iter=5) # bad at both
    #rfc = svm.SVC() # lineage ok, subtypes are nonsense
    rfc.fit(train_data, train_lineage)
    pred_lineage = rfc.predict(test_data)

    rfc = RandomForestClassifier(max_depth=2, random_state=0)
    #rfc = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,2), random_state=1)
    #rfc = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
    #rfc = svm.SVC()
    rfc.fit(train_data, train_subtype)
    pred_subtype = rfc.predict(test_data)

    print(samples[test_idx]["filename"], samples[test_idx]["lineage"], samples[test_idx]["subtype"], "Predicted:", pred_lineage[0], pred_subtype[0])
