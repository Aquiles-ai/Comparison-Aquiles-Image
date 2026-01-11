# This repository provides all the files to reproduce all the tests presented in the blog post *["Horizontal Scaling for Self-Hosted Image Generation"](https://aquiles-ai.vercel.app/blog/Aquiles-Image-horizontal-scaling)*

All files that are `deploy_*.py` are for deploying Aquiles-Image with Modal.

### How to deploy on Modal?

To deploy on Modal, first go to the [Modal website](https://modal.com) and create an account.

Then set it up on your local machine with these commands:
```bash
# Install Modal SDK
uv pip install modal

# Authenticate
python3 -m modal setup
```

Ideally, in the modal dashboard, configure the `huggingface-secret` with your huggingface token to download models and avoid restricted access issues.

Now, to deploy, just use this command:

```bash
# Replace with the deployment file you'll use
modal deploy deploy_*.py
```