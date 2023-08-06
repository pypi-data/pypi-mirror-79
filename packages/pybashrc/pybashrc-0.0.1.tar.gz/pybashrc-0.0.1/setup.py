import setuptools


def setup():
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="pybashrc",
        version="0.0.1",
        author="Jelmer Neeven",
        author_email="author@example.com",
        description="Register python functions as bash commands",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jneeven/pybashrc",
        packages=setuptools.find_packages(),
        package_data={
            # If any package contains *.txt or *.rst files, include them:
            "": [
                ".pybashrc_aliases",
                ".pybashrc_execute.py",
                "alias_template",
                "bashrc_template",
            ],
        },
        entry_points={"console_scripts": ["pybash=pybashrc.post_setup:post_setup"]},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix ",
        ],
        python_requires=">=3.6",
    )


if __name__ == "__main__":
    setup()
