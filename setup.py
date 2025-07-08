import os
from typing import List

from setuptools import setup, find_packages

def get_path_to_this_files_parent_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_path_to_requirements_txt_relative_to_this_file() -> str:
    return os.path.join(get_path_to_this_files_parent_dir(), "requirements.txt")


def load_required_packages_from_requirements_txt() -> List[str]:
    with open(get_path_to_requirements_txt_relative_to_this_file(), "r") as file:
        return [ln.strip() for ln in file.readlines()]


def get_version_number() -> str:
    with open("CODE_VERSION.cfg") as version_file:
        version = version_file.read().strip()
    return version

setup(
    name='market-beacon',
    version=get_version_number(),
    author='David Young',
    description='TODO',
    url='https://github.com/the-user-created/market-beacon',
    packages=find_packages(),
    package_dir={"market-beacon": "market-beacon"},
    package_data={
        "market-beacon": [
            # If you want to add data to the package, put the path to it relative to the package here
        ]
    },
    install_requires=load_required_packages_from_requirements_txt(),
    extras_require={
        "dev": [
            "bump2version==1.0.1",
            "black==25.1.0",
            "isort==6.0.1",
            "flake8==7.3.0",
            "pre-commit==4.2.0",
        ]
    },
    python_requires=">=3.12",
)
