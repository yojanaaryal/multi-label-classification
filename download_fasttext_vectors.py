"""Fetch the official pretrained 300-D English fastText vectors."""
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
DEST = ROOT / ".venv" / "models" / "fasttext" / "wiki-news-300d-1M-subword.vec.zip"
URL = "https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M-subword.vec.zip"

DEST.parent.mkdir(parents=True, exist_ok=True)
if DEST.exists() and DEST.stat().st_size > 100_000_000:
    print(f"FastText archive already exists: {DEST} ({DEST.stat().st_size:,} bytes)")
else:
    partial = DEST.with_suffix(DEST.suffix + ".part")
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as out:
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                downloaded += len(chunk)
                if total:
                    print(f"Downloaded {downloaded:,}/{total:,} bytes", end="\r", flush=True)
        partial.replace(DEST)
        print(f"\nSaved FastText vectors to {DEST} ({DEST.stat().st_size:,} bytes)")
    except Exception as exc:
        partial.unlink(missing_ok=True)
        raise SystemExit(
            "FastText download failed. This runtime must be able to reach dl.fbaipublicfiles.com. "
            f"Details: {exc}"
        ) from exc
