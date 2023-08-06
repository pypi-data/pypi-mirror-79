# pybashrc: Automatically register python functions as bash commands
This is a very simple utility that will create a `~/.pybashrc.py` file, and any functions it contains will be accessible as a bash command. For example, take a look at the [pybashrc template file](pybashrc/pybashrc_template.py):
```python
# Pybashrc file. Create your command-line accessible python functions here.
def _hidden_print_function(*args):
    """This function will be ignored by pybashrc, and will not be available from the
    command line.
    However, other functions can still use it.
    """
    print(*args)


def test_pybashrc(first_argument: str, second_argument: str = "second_argument"):
    """Default test function that simply prints its input arguments. This only serves as
    an example of how to define pybashrc functions.
    Arguments:
        - first_argument (str): The first argument.
        - second_argument (str): The second argument, which has a default value.
    """
    _hidden_print_function("This is the pybash default test function.")
    _hidden_print_function(f"Provided arguments: {first_argument}, {second_argument}")
```

Since `test_pybashrc` is defined in this file and does not start with a `_`, it will be accessible as a bash command:
```
$ pybash
Available functions:
- test_pybashrc(first_argument: str, second_argument: str = 'second_argument')
	Default test function that simply prints its input arguments. This only serves as an example of how to define pybashrc functions.

	Arguments:
		- first_argument (str): The first argument.
		- second_argument (str): The second argument, which has a default value.
	
```

```
$ test_pybashrc arg1 arg2
This is the pybash default test function.
Provided arguments: arg1, arg2
```

## Installation
Simply run `pip install pybashrc`, and then run `pybashrc` once to set up the bash alias files etc. After that, you're ready to go! Any time you update your `.pybashrc.py`, you only need to restart the shell to process the updates.

## TODO:
- [ ] Print function info if we get a TypeError when calling it
- [ ] Support click commands
- [ ] Support running from a virtual environment?
