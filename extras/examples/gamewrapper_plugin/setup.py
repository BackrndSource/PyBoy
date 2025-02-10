from setuptools import setup

setup(
    name="pyboy-gamewrapper-example",
    version="0.1",
    py_modules=["plugin"],
    # install_requires=["pyboy"],
    entry_points={
        "pyboy_plugins": [
            "gamewrapper_example = plugin:ExamplePyBoyGameWrapperPlugin",
        ],
    },
)
