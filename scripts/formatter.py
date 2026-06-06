import os

os.system('python -m black .')
os.system('python -m isort .')
os.system('python -m flake8')
