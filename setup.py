import os

import pip

package = 'pipenv'
try:
    __import__(package)
except ImportError:
    pip.main(['install', package])

os.system('pipenv install --system')
