## Running on METR-LA and PEMS-BAY

This repository was originally designed for PEMS datasets (flow). To run it on **METR-LA** and **PEMS-BAY** (speed datasets), the following preprocessing and compatibility steps were applied.

---

### 1. Data Preparation

Place raw data in:

```
FOGS/data/METRLA/
FOGS/data/PEMSBAY/
```

#### METR-LA

Required files:

* `metr_la.npz`
* `distances_la.csv` → converted to `METRLA_fixed.csv` (remapped sensor IDs)
* `METRLA_flow_count.pkl` (mean speed per node)

#### PEMS-BAY

Required files:

* `pems_bay.npz`
* `pems_bay_spatial_distance.npy` → converted to `PEMSBAY.csv`
* `PEMSBAY_flow_count.pkl`

> Note: For PEMS-BAY, `inf` distances are removed when converting `.npy → CSV`.

---

### 2. Graph Construction

Run:

```bash
cd node2vec-master/scripts
```

#### METR-LA

```bash
python graph_preparation.py \
  --num_of_vertices 207 \
  --distances_filename ../../data/METRLA/METRLA_fixed.csv \
  --data_filename ../../data/METRLA/METRLA.npz \
  --edgelist_filename ../graph/METRLA.edgelist \
  --filename_T ../graph/METRLA_graph_T.npz \
  --flow_mean ../../data/METRLA/METRLA_flow_count.pkl
```

#### PEMS-BAY

```bash
python graph_preparation.py \
  --num_of_vertices 325 \
  --distances_filename ../../data/PEMSBAY/PEMSBAY.csv \
  --data_filename ../../data/PEMSBAY/pems_bay.npz \
  --edgelist_filename ../graph/PEMSBAY.edgelist \
  --filename_T ../graph/PEMSBAY_graph_T.npz \
  --flow_mean ../../data/PEMSBAY/PEMSBAY_flow_count.pkl
```

> ⚠️ Important: remove the `if not exists(edgelist)` condition in `graph_preparation.py` or delete existing `.edgelist` before running, otherwise `graph_T` will not be generated.

---

### 3. Node2Vec Embedding

```bash
cd ../src
```

```bash
python main_tra.py \
  --input ../graph/<DATASET>.edgelist \
  --input_T ../graph/<DATASET>_graph_T.npz \
  --output ../emb/<DATASET>.emb
```

---

### 4. Learned Graph Construction

```bash
cd ../scripts
```

```bash
python learn_graph.py \
  --filename_emb ../emb/<DATASET>.emb \
  --output_pkl_filename ../../data/<DATASET> \
  --thresh_cos 10 \
  --num_nodes <N>
```

Where:

* `N = 207` for METR-LA
* `N = 325` for PEMS-BAY

> Fix applied: handle missing node embeddings and map node IDs correctly when building `learn_mx.pkl`.

---

### 5. Dataset Generation

```bash
cd ../../STFGNN
```

```bash
python generate_datasets.py \
  --output_dir ../data/processed/<DATASET>/ \
  --flow_mean ../data/<DATASET>/<DATASET>_flow_count.pkl \
  --traffic_df_filename ../data/<DATASET>/<data_file>.npz
```

---

### 6. Training

Update:

```python
DATASET = '<DATASET>'
```

Then run:

```bash
python train.py
```

---

### Notes / Fixes Applied

* Converted **Conv1d → Conv2d** in temporal module to support 4D tensors
* Fixed deprecated NumPy types (`np.int → np.int32`)
* Ensured graph sizes match dataset (`207 / 325`)
* Handled missing node embeddings in `learn_graph.py`
* Removed silent skipping of temporal graph generation
* Adjusted file paths for relative execution (`../data/...`)

---
