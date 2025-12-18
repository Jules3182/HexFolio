import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def load_yaml(path: Path):
    with open(path) as f:
        return yaml.safe_load(f)

# One source of truth for using the user's config 
CONFIG = load_yaml(BASE_DIR / "config.yaml")
HOLDINGS_DATA = load_yaml(BASE_DIR / "holdings.yaml")