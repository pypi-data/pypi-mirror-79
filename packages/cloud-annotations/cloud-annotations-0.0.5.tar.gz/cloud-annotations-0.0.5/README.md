# Cloud Annotations Python SDK

source env/bin/activate

rm -rf dist
python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*
