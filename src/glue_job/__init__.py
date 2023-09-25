import os

GLUE_ROOT = os.path.abspath(os.path.dirname(__file__))
SRC_ROOT = os.path.abspath(os.path.join(GLUE_ROOT, os.pardir))
ROOT = os.path.abspath(os.path.join(GLUE_ROOT, os.pardir))

print(GLUE_ROOT)
