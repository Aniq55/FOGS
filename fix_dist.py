import pandas as pd
import numpy as np

# ===== PATHS (EDIT IF NEEDED) =====
DATA_DIR = "/home/chri6578/Documents/aniq/DATA/METRLA"

dist_path = f"{DATA_DIR}/distances_la.csv"
loc_path = f"{DATA_DIR}/graph_sensor_locations.csv"
npz_path = f"{DATA_DIR}/metr_la.npz"

output_path = f"{DATA_DIR}/METRLA_fixed.csv"

# ===== STEP 1: LOAD FILES =====
print("Loading files...")
df = pd.read_csv(dist_path)
loc = pd.read_csv(loc_path)
X = np.load(npz_path)['data']

print("Distance file shape:", df.shape)
print("Location file shape:", loc.shape)
print("NPZ shape:", X.shape)

# ===== STEP 2: GET SENSOR IDS =====
# Try to automatically find the correct column
print("\nLocation columns:", loc.columns.tolist())

if 'sensor_id' in loc.columns:
    sensor_ids = loc['sensor_id'].values
elif 'id' in loc.columns:
    sensor_ids = loc['id'].values
else:
    raise ValueError("Couldn't find sensor ID column in graph_sensor_locations.csv")

print("Number of sensors from location file:", len(sensor_ids))

# ===== STEP 3: FILTER DISTANCE FILE =====
print("\nFiltering distance file...")

# Ensure types match
df['from'] = df['from'].astype(int)
df['to'] = df['to'].astype(int)

sensor_set = set(sensor_ids)

df_filtered = df[
    df['from'].isin(sensor_set) &
    df['to'].isin(sensor_set)
]

print("Filtered edges:", len(df_filtered))

# ===== STEP 4: VERIFY NODE COUNT =====
nodes = sorted(set(df_filtered['from']).union(set(df_filtered['to'])))
print("Unique nodes after filtering:", len(nodes))

if len(nodes) != len(sensor_ids):
    print("WARNING: Node count mismatch!")
    print("Expected:", len(sensor_ids), "Got:", len(nodes))

# ===== STEP 5: CREATE MAPPING =====
print("\nCreating node mapping...")

node_to_idx = {node: i for i, node in enumerate(sensor_ids)}

# ===== STEP 6: APPLY MAPPING =====
df_filtered['from'] = df_filtered['from'].map(node_to_idx)
df_filtered['to'] = df_filtered['to'].map(node_to_idx)

# ===== STEP 7: FINAL CHECK =====
print("\nAfter mapping:")
print(df_filtered.head())

mapped_nodes = set(df_filtered['from']).union(set(df_filtered['to']))
print("Final node indices:", len(mapped_nodes))
print("Min index:", min(mapped_nodes), "Max index:", max(mapped_nodes))

# ===== STEP 8: SAVE =====
df_filtered.to_csv(output_path, index=False)

print("\n✅ DONE")
print("Saved to:", output_path)