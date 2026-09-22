from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from huggingface_hub import hf_hub_download


RELEASE_VERSION = "cadence-models-v1"

MODELS = (
    {
        "tier": "preferred1b",
        "repo_id": "litert-community/Gemma3-1B-IT",
        "revision": "a6306a4e292016480083b73b8dc6f3f939ae04c3",
        "filename": "Gemma3-1B-IT_multi-prefill-seq_q4_ekv4096.litertlm",
        "sha256": "1325ae366d31950f137c9c357b9fa89448b176d76998180c08ceaca78bba98be",
    },
    {
        "tier": "fallback270m",
        "repo_id": "litert-community/gemma-3-270m-it",
        "revision": "9d2093270fb5aa49a986b49b5779d763dde7b630",
        "filename": "gemma3-270m-it-q8.litertlm",
        "sha256": "757e9119fa5bd667a2774fb470ac4afcd3190a21c677f8e69a5d6bc908abdd63",
    },
)


def digest(path: Path) -> tuple[int, str]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            hasher.update(chunk)
    return size, hasher.hexdigest()


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("HF_TOKEN is required as a private release secret")

    root = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="cadence-model-release-") as temp:
        staging = Path(temp)
        manifest_models = []
        for model in MODELS:
            downloaded = Path(
                hf_hub_download(
                    repo_id=model["repo_id"],
                    filename=model["filename"],
                    revision=model["revision"],
                    token=token,
                    local_dir=staging,
                    local_dir_use_symlinks=False,
                )
            )
            size, actual_hash = digest(downloaded)
            if size <= 0 or actual_hash != model["sha256"]:
                raise SystemExit(
                    f"Pinned digest mismatch for {model['filename']}: "
                    f"size={size}, sha256={actual_hash}"
                )
            destination = root / model["filename"]
            shutil.copy2(downloaded, destination)
            manifest_models.append(
                {
                    "tier": model["tier"],
                    "modelId": model["filename"],
                    "sourceRepository": model["repo_id"],
                    "sourceRevision": model["revision"],
                    "assetFileName": model["filename"],
                    "byteSize": size,
                    "sha256": actual_hash,
                }
            )

    for required in (root / "NOTICE", root / "GEMMA-TERMS.md"):
        if not required.is_file() or required.stat().st_size == 0:
            raise SystemExit(f"Required release file is missing or empty: {required}")

    (root / "model-manifest.json").write_text(
        json.dumps(
            {"releaseVersion": RELEASE_VERSION, "models": manifest_models},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
