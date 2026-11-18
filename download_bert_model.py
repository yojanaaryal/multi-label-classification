"""Download bert-base-uncased into the project virtual environment's model folder."""
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parent
ENV_DIR = ROOT / ".venv"
MODEL_DIR = ENV_DIR / "models" / "bert-base-uncased"
HF_HOME = ENV_DIR / "huggingface"

os.environ["HF_HOME"] = str(HF_HOME)
os.environ["HUGGINGFACE_HUB_CACHE"] = str(HF_HOME / "hub")

try:
    from huggingface_hub import snapshot_download
except ImportError as exc:
    raise SystemExit(
        f"Install huggingface_hub in this environment first: {ENV_DIR}/bin/python -m pip install huggingface_hub"
    ) from exc

try:
    path = snapshot_download(
        repo_id="google-bert/bert-base-uncased",
        local_dir=MODEL_DIR,
        allow_patterns=[
            "config.json",
            "model.safetensors",
            "pytorch_model.bin",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.txt",
            "added_tokens.json",
        ],
    )
except Exception as exc:
    raise SystemExit(
        "BERT download failed. Check network access to huggingface.co and rerun "
        f"with {ENV_DIR}/bin/python {Path(__file__).name}.\nDetails: {exc}"
    ) from exc

print(f"Downloaded BERT checkpoint to: {path}")
