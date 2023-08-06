import setuptools

def get_long_description():
    with open("README.md", "r") as readme_file:
        return readme_file.read()

setuptools.setup(
    name="red-green-refactor-widget",
    version="0.0.1",
    author="Andrey Krainyak",
    author_email="mode.andrew@gmail.com",
    description=\
        "A simple widget that will help you to stick to "
        "the red-green-refactor workflow",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="http://github.com/mode89/red-green-refactor-widget",
    packages=setuptools.find_packages(),
    package_data={ "red_green_refactor_widget": [ "window.ui" ] },
    include_pacakge_data=True,
    install_requires=[
        "PyQt5",
        "pyqtkeybind",
    ],
    entry_points={
        "console_scripts":
            ["red-green-refactor-widget=red_green_refactor_widget.cli:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
