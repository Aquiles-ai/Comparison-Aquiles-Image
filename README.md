# Test Reproduction for Horizontal Scaling

This repository contains all the necessary files to reproduce the tests presented in the blog post *["Horizontal Scaling for Self-Hosted Image Generation"](https://aquiles-ai.vercel.app/blog/Aquiles-Image-horizontal-scaling)*.

Files following the `deploy_*.py` pattern are designed to deploy Aquiles-Image using Modal.

## How to Deploy on Modal

### Step 1: Create an Account

First, visit the [Modal website](https://modal.com) and create an account.

### Step 2: Set Up Modal Locally

Configure Modal on your local machine by running the following commands:
```bash
# Install the Modal SDK
uv pip install modal

# Authenticate your account
python3 -m modal setup
```

### Step 3: Configure Secrets

In the Modal dashboard, configure the `huggingface-secret` with your Hugging Face token. This allows you to download models and avoid restricted access issues.

### Step 4: Deploy

To deploy, simply run the following command:
```bash
# Replace with the deployment file you want to use
modal deploy deploy_*.py
```

## Running the Tests

### Step 1: Create Environment File

First, create a `.env` file in the root of the repository with the URL you obtained after deploying your chosen configuration on Modal:
```env
URL_MODAL="https://your-user--aquiles-image-server-serve.modal.run"
```

### Step 2: Execute Tests

Run the test file you want to try:
```bash
# Replace with the test file you want to use
python test_*.py
```