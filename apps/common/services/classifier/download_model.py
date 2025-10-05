# downloader.py
import os
from huggingface_hub import snapshot_download

# Model info
REPO_ID = "facebook/bart-large-mnli"
REVISION = "d7645e127eaf1aefc7862fd59a17a5aa8558b8ce"  # exact pinned commit SHA

# Local target
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models", "bart-mnli")

print(MODEL_DIR)

# Download snapshot
snapshot_path = snapshot_download(
    repo_id=REPO_ID,
    revision=REVISION,
    cache_dir=MODEL_DIR,
    local_dir_use_symlinks=False
)

# Save a pointer file with the actual snapshot path
with open(os.path.join(MODEL_DIR, "SNAPSHOT_PATH.txt"), "w") as f:
    f.write(snapshot_path)

with open(os.path.join(MODEL_DIR, "MODEL_PIN.txt"), "w") as f:
    f.write(f"{REPO_ID}@{REVISION}\n")

print("Model downloaded to:", snapshot_path)
