# Publish manually

This folder is intentionally not a Git repository. Run these commands from
this directory after confirming the Git identity shown by the first two
commands:

```bash
cd /Users/vini/Documents/development/zoocha/cadence-model-assets
git config user.name
git config user.email
```

If either value is not your GitHub identity, set it locally before committing:

```bash
git config user.name "YOUR GITHUB NAME"
git config user.email "YOUR VERIFIED GITHUB EMAIL"
```

Then initialize and publish the public repository:

```bash
git init -b main
git add README.md NOTICE GEMMA-TERMS.md .gitignore .github PUBLISHING.md
git commit -m "chore: add public model release workflow"
gh auth login -h github.com
gh repo create ViniciusMacedoCamara/cadence-model-assets \
  --public \
  --description "Versioned public model assets for Cadence local semantic extraction" \
  --source . \
  --remote origin \
  --push
```

The repository will exist after that command, but `cadence-models-v1` will
still be blocked until:

1. `GEMMA-TERMS.md` is replaced with the reviewed applicable Gemma terms.
2. The repository Actions secret `HF_TOKEN` is configured with access to the
   pinned upstream model files.
3. The `model-release` environment is approved, if environment protection is
   enabled.
4. The `Publish pinned Gemma assets` workflow is manually dispatched.

Do not add `.litertlm` binaries to Git history. The workflow downloads them in
its temporary workspace, verifies their exact SHA-256 values and byte sizes,
and uploads them only to the immutable GitHub Release.
