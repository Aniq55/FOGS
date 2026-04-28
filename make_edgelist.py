import pandas as pd

# paths
input_csv = "/home/chri6578/Documents/aniq/FOGS/data/PEMSBAY/PEMSBAY.csv"
output_file = "/home/chri6578/Documents/aniq/FOGS/node2vec-master/graph/PEMSBAY.edgelist"

df = pd.read_csv(input_csv)

# check columns
print(df.columns)

# assume columns: from, to, distance (or cost)
edges = df[['from', 'to']].values

with open(output_file, "w") as f:
    for i, j in edges:
        f.write(f"{int(i)} {int(j)}\n")

print("✅ edgelist created:", output_file)
print("Number of edges:", len(edges))