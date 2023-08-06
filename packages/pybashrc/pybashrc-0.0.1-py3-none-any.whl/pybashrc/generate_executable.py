import os
from pathlib import Path

_INSTALL_DIR = Path(os.environ["PYBASHRC_INSTALL_DIR"])


def generate_executable():
    # Read contents of pybash file
    pybash_file = Path.home() / ".pybashrc.py"
    pybash = pybash_file.read_text().replace("    ", "\t") + "\n\n"

    # Read the pybash execute file template
    execute = (_INSTALL_DIR / "execute_template.py").read_text().replace("    ", "\t")

    # Create pybash execute file consisting of pybash file and a main function that
    # calls the appropriate user functions
    execute_file = _INSTALL_DIR / ".pybashrc_execute.py"
    execute_file.write_text(f"{pybash}\n\n{execute}")


if __name__ == "__main__":
    generate_executable()
