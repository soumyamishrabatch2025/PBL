"""Run the project without an editable installation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from sentiment_research.cli import main

if __name__ == "__main__":
    main()
