from setuptools import setup, find_packages

setup(
    name="mira_sdk",  # Keep underscore here for Python import
    version='0.1.12',  # Match version with pyproject.toml
    description="A Python SDK for the Mira API",
    long_description=open("README.md").read(),
    url="https://github.com/Aroha-Labs/mira-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="==3.10.*",
    install_requires=[
        "pyyaml>=6.0.2",
        "requests>=2.32.3",
        "semantic-version>=2.10.0",
        "aiohttp>=3.10.10",
        "pytest-asyncio>=0.24.0",
    ],
)
