#!/usr/bin/env bash
set -x
set -e

pip3 install -r docs/requirements.txt

cd docs
PYTHONPATH=../ mkdocs build
cd ..
python3 scripts/modify_sitemap.py