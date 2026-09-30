#!/usr/bin/env bash
set -x
set -e

pip3 install --break-system-packages -r docs/requirements.txt

cd docs
PYTHONPATH=../ python3 -m mkdocs build
cd ..
python3 scripts/modify_sitemap.py