"""Download the exact raw SentiMix source files used by this experiment."""
import hashlib
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data/raw/hinglish_24k_sources/sentimix"
BASE = "https://raw.githubusercontent.com/JunKong5/Semveal2020-task9/master/sentimix/dataprocess/hindi/data/"
FILES = {
    "train_14k_split_conll.txt": "b2bc9e9e2494693ab3b0fd025ffb0292a3c4ab959861306dd1d993fa7e7c2177",
    "dev_3k_split_conll.txt": "9679768e0b6697be4c492b41f876756023fdb0face8cb86f8cd6cdb767acd1dc",
}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    for name, expected in FILES.items():
        target = DEST / name
        if target.exists():
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise ValueError(f"Existing raw file differs from the recorded source: {target}")
            print("Already verified:", target)
            continue
        for attempt in range(3):
            try:
                with urllib.request.urlopen(BASE + name, timeout=90) as response:
                    data = response.read()
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(2)
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"Upstream file changed or download incomplete: {name}; file not saved")
        target.write_bytes(data)
        print("Downloaded and verified:", target)


if __name__ == "__main__":
    main()
