#SHARED PATH CONSTANTS - resolved relative to this file so scripts work
#regardless of the working directory they're launched from
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / 'data_exports'
SECRETS_DIR = PROJECT_ROOT / 'secrets'
