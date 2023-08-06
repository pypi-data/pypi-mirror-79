# <START OF PYBASHRC CODE>
export PYBASHRC_INSTALL_DIR="<INSTALL_DIR>"
# Include pybashrc alias file if it exists
if [ -d $PYBASHRC_INSTALL_DIR/ ]; then
    # Generate pybashrc executable file based on .pybashrc.py
    python3 $PYBASHRC_INSTALL_DIR/generate_executable.py
    # Update pybashrc alias file to include all functions
    python3 $PYBASHRC_INSTALL_DIR/.pybashrc_execute.py _update_aliases
    # Include aliases in this bashrc
    . $PYBASHRC_INSTALL_DIR/.pybashrc_aliases
fi
# <END OF PYBASHRC CODE>
