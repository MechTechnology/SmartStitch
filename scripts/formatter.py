import os

os.system('python -m black . --skip-string-normalization')
os.system('python -m isort .')
os.system('python -m flake8')
