from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()

    setup(
        name="martys_nim_challenge",
        version="0.0.1",
        description="Try to beat my AI in a game of Nim!",
        long_description=readme(),
        long_description_content_type="text/markdown",
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            'Programming Language :: Python :: 3.9'
        ],
        url
    )