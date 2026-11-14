import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "web"))

from web.app import app
