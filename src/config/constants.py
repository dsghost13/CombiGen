from pathlib import Path

from PyQt6.QtWidgets import QSizePolicy

# size policy
E = QSizePolicy.Policy.Expanding
F = QSizePolicy.Policy.Fixed
P = QSizePolicy.Policy.Preferred

# file paths
PROJECT_DIR = Path(__file__).resolve().parents[2]
SCRIPT_PATH = PROJECT_DIR / "script.py"
TXT_PATH = PROJECT_DIR / "output.txt"
CSV_PATH = PROJECT_DIR / "output.csv"
SCAN_PATH = PROJECT_DIR / "src" / "scriptgen" / "script_scan.py"

# colors
COLORS = {
    "DARK_GRAY":   "#303030",
    "DARKER_GRAY": "#202020",
    "BLACK":       "#000000",
    "WHITE":       "#FFFFFF",
    "DARK_GREEN":  "#007800",
    "LIGHT_GREEN": "#009900",
    "DARK_RED":    "#9C0A00",
    "LIGHT_RED":   "#B30F00",
    "DARK_BLUE":   "#2C59C8",
    "MEDIUM_BLUE": "#3B74F0",
    "LIGHT_BLUE":  "#3B8BF5"
}