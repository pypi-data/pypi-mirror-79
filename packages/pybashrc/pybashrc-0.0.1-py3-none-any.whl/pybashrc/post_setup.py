import re
from pathlib import Path

INSTALL_DIR = Path(__file__).parent


def update_bashrc():
    bashrc = Path.home() / ".bashrc"
    contents = bashrc.read_text()
    to_write = (INSTALL_DIR / "bashrc_template").read_text()

    contents, replacements = re.subn(
        r"\# \<START OF PYBASHRC CODE\>\n(.|\n)*\n\# \<END OF PYBASHRC CODE\>\n",
        to_write,
        contents,
    )
    if replacements == 0:
        contents += "\n" + to_write

    bashrc.write_text(contents.replace("<INSTALL_DIR>", str(INSTALL_DIR.absolute())))
    print(f"Modified {bashrc}")


def post_setup():
    pybashrc_file = Path.home() / ".pybashrc.py"
    if not pybashrc_file.exists():
        pybashrc_file.write_text((INSTALL_DIR / "pybashrc_template.py").read_text())
        print(f"Created pybashrc file at {pybashrc_file}.")

    alias_file = INSTALL_DIR / ".pybashrc_aliases"
    alias_file.write_text((INSTALL_DIR / "alias_template").read_text())
    print(f"Created pybashrc alias file at {alias_file}.")

    update_bashrc()

    print("pybashrc post-install setup complete. Please restart your shell.")
