import os

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_BASE = os.path.join(BASE_DIR, "common", "services", "classifier", "models", "bart-mnli")

SNAPSHOT_ROOT = os.path.join(MODEL_BASE, "models--facebook--bart-large-mnli", "snapshots")

snapshots = os.listdir(SNAPSHOT_ROOT)
if not snapshots:
    raise RuntimeError(f"No snapshots found in {SNAPSHOT_ROOT}. Run downloader.py first.")

SNAPSHOT_DIR = os.path.join(SNAPSHOT_ROOT, snapshots[0])
print("Loading model from:", SNAPSHOT_DIR)

tokenizer = AutoTokenizer.from_pretrained(SNAPSHOT_DIR, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(SNAPSHOT_DIR, local_files_only=True)
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)


def get_pinned_model_rev():
    pin_file = os.path.join(MODEL_BASE, "MODEL_PIN.txt")
    if os.path.exists(pin_file):
        return open(pin_file).read().strip()
    return None


print("Pinned revision:", get_pinned_model_rev())
