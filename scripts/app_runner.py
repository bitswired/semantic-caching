import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main():
    path = Path(__file__).parent / "app.py"
    sys.argv = ["streamlit", "run", str(path)]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
