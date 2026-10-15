"""Compatibility entry point; prefer python build_pdfs.py station1 station4."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from printkit.pipeline import main
if __name__ == '__main__':
    main(['station1', 'station4'])
