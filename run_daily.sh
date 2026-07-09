#!/bin/bash

source .venv/bin/activate
cd "$(dirname "$0")"

export OPENAI_API_KEY="ollama"
export OPENAI_BASE_URL="http://localhost:11434/v1"
export MODEL_NAME="qwen3.5:9b"
export CATEGORIES="cs.CL, cs.AI"
export LANGUAGE="Chinese"
export EMAIL="kklb1716@gmail.com"
export NAME="ouotingwei"

git pull
bash run.sh

# 推回 GitHub
today=$(date -u "+%Y-%m-%d")
git add .
git commit -m "auto: daily arXiv update ${today}" || echo "沒有新變更,略過 commit"
git push
