import pathlib
from setuptools import find_packages, setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cryptowatch-sdk",
    version="0.0.14",
    description="Python bindings for the Cryptowatch API. Cryptocurrency markets, assets, instruments and exchanges data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cryptowatch/cw-sdk-python",
    author="Cryptowatch",
    author_email="infra@cryptowat.ch",
    keywords="cryptowatch sdk bitcoin crypto",
    license="BSD-2",
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "marshmallow >= 3.2.2",
        "requests >= 2.22.0",
        "PyYAML >= 5.1.2",
        "urllib3 >= 1.25.7",
        "websocket-client >= 0.56.0",
        "protobuf >= 3.11.3",
    ],
    packages=find_packages(exclude=("tests", "examples")),
    entry_points={"console_scripts": ["cryptowatch=cryptowatch.__main__:main",]},
    python_requires=">=3.7",
    project_urls={
        "Bug Tracker": "https://github.com/cryptowatch/cw-sdk-python/issues",
        "Documentation": "https://github.com/cryptowatch/cw-sdk-python#installation",
        "Source Code": "https://github.com/cryptowatch/cw-sdk-python",
    },
    tests_require=["pytest >= 5.3.1", "pytest-mock >= 1.12", "requests-mock >= 1.7"],
)
