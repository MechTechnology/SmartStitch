import os

os.system('python -m black . --skip-string-normalization --line-length 120 --exclude .venv --target-version py310')
os.system('python -m isort . --profile black --line-length 120 --skip .venv')
os.system('python -m flake8 --max-line-length 120 --ignore E501 --exclude .venv,__pycache__')
