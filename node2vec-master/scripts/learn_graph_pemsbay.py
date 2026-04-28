import pickle
import argparse
import numpy as np
import os


def get_cos_similar(v1, v2):
    num = float(np.dot(v1, v2))
    denom = np.linalg.norm(v1) * np.linalg.norm(v2)
    return 0.5 + 0.5 * (num / denom) if denom != 0 else 0


def learn_final_graph(threshold, filename, direct, full_num_nodes):
    def readEmbedFile(embedFile):
        with open(embedFile, 'r') as f:
            lines = f.readlines()

        embeddings = {}
        for lineId in range(1, len(lines)):  # skip header
            splits = lines[lineId].strip().split()
            embedId = int(splits[0])
            embedValue = [float(x) for x in splits[1:]]
            embeddings[embedId] = embedValue

        return embeddings

    embeddings = readEmbedFile(filename)

    # ✔ correct: use actual node IDs
    index_list = sorted(embeddings.keys())
    num_nodes = len(index_list)

    print(f"Embeddings found: {num_nodes}/{full_num_nodes}")

    cos_mx = np.zeros((num_nodes, num_nodes), dtype=np.float32)

    # ✔ compute cosine similarity using real node IDs
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            node_i = index_list[i]
            node_j = index_list[j]

            embedding_i = np.asarray(embeddings[node_i])
            embedding_j = np.asarray(embeddings[node_j])

            cos_value = get_cos_similar(embedding_i, embedding_j)
            cos_mx[i][j] = cos_mx[j][i] = cos_value

    # ✔ build learned graph (KNN)
    learn_mx_small = np.zeros((num_nodes, num_nodes), dtype=np.float32)

    for row in range(num_nodes):
        indices = np.argsort(cos_mx[row])[::-1][:threshold]
        norm = cos_mx[row, indices].sum()

        if norm == 0:
            continue

        for idx in indices:
            learn_mx_small[row, idx] = cos_mx[row, idx] / norm

    # ✔ expand back to full graph size
    learn_mx_full = np.zeros((full_num_nodes, full_num_nodes), dtype=np.float32)

    for i in range(num_nodes):
        for j in range(num_nodes):
            node_i = index_list[i]
            node_j = index_list[j]
            learn_mx_full[node_i, node_j] = learn_mx_small[i, j]

    if not direct:
        learn_mx_full = np.maximum.reduce([learn_mx_full, learn_mx_full.T])
        print('Final graph is undirected')
    else:
        print('Final graph is directed')

    return learn_mx_full


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename_emb', type=str, required=True)
    parser.add_argument('--output_pkl_filename', type=str, required=True)
    parser.add_argument('--thresh_cos', type=int, default=10)
    parser.add_argument('--direct_L', type=bool, default=True)
    parser.add_argument('--num_nodes', type=int, required=True)  # ✔ NEW

    args = parser.parse_args()

    output_pkl_filename = args.output_pkl_filename + '/' + 'learn_mx.pkl'
    print(output_pkl_filename)

    if os.path.exists(args.filename_emb):
        learn_graph = learn_final_graph(
            threshold=args.thresh_cos,
            filename=args.filename_emb,
            direct=args.direct_L,
            full_num_nodes=args.num_nodes
        )

        with open(output_pkl_filename, 'wb') as f:
            pickle.dump(learn_graph, f, protocol=2)

        print("Saved learned graph:", learn_graph.shape)