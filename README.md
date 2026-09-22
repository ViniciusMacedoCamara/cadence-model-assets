# Cadence model assets

Public, versioned model distribution metadata for Cadence's optional local
semantic extraction feature.

The Cadence app downloads model bytes from immutable GitHub Releases. It does
not send prescription images, OCR text, medicine data, or user identifiers to
this repository. Model binaries are deliberately not committed to Git history.

## Release contract

The first release is `cadence-models-v1` and contains exactly these assets:

```text
Gemma3-1B-IT_multi-prefill-seq_q4_ekv4096.litertlm
gemma3-270m-it-q8.litertlm
NOTICE
GEMMA-TERMS.md
model-manifest.json
```

The release is created manually by
`.github/workflows/publish-models.yml`. The workflow downloads the pinned
upstream revisions with the private `HF_TOKEN` Actions secret, verifies exact
byte sizes and SHA-256 digests, generates the manifest, and uploads only the
five release assets. The secret is never written to the repository or logged.

The release is not ready until `GEMMA-TERMS.md` contains the applicable Gemma
Terms of Use after redistribution review. See
[`GEMMA-TERMS.md`](GEMMA-TERMS.md) and [`NOTICE`](NOTICE).

## Pinned sources

| Tier | Source revision | Release asset | SHA-256 |
| --- | --- | --- | --- |
| Preferred 1B Q4 | `a6306a4e292016480083b73b8dc6f3f939ae04c3` | `Gemma3-1B-IT_multi-prefill-seq_q4_ekv4096.litertlm` | `1325ae366d31950f137c9c357b9fa89448b176d76998180c08ceaca78bba98be` |
| Fallback 270M Q8 | `9d2093270fb5aa49a986b49b5779d763dde7b630` | `gemma3-270m-it-q8.litertlm` | `757e9119fa5bd667a2774fb470ac4afcd3190a21c677f8e69a5d6bc908abdd63` |

The upstream repositories are `litert-community/Gemma3-1B-IT` and
`litert-community/gemma-3-270m-it` on Hugging Face. The end user does not need
a Hugging Face account or token.
