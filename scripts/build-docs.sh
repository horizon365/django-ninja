#!/usr/bin/env bash
set -x
set -e

pip install -r docs/requirements.txt

cd docs
PYTHONPATH=../ mkdocs build
cd ..
python scripts/modify_sitemap.py