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
        license="MIT",
        classifiers=[
            "Development Status :: 4 - Beta",
            "License :: OSI Approved :: MIT License",
            'Programming Language :: Python :: 3.9'
        ],
        url="https://github.com/MartinStoller/Nim_AI_Challenge",
        author="MartinStoller",
        author_email="martin.stoller2@gmx.de",
        keywords="AI Nim Challenge YouTube",
        packages=["nim_yt"],  # TODO
        install_requires=[pygame],  # TODO
        include_package_data=True,
        zip_safe=False
    )
