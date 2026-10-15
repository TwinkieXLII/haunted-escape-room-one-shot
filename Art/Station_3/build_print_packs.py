"""Compatibility entry point. Prefer python build_pdfs.py station3."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from printkit.pipeline import main
if __name__ == '__main__':
    main(['station3'])
