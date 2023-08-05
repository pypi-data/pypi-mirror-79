import os
import setuptools

current_directory = os.path.abspath(os.path.dirname(__file__))


with open("README.rst", "r") as fh:
    long_description = fh.read()


def get_install_requirements():
    requirements_path = os.path.join(current_directory, "requirements.txt")
    with open(requirements_path, encoding="utf-8") as fp:
        return fp.read().splitlines()


setuptools.setup(
    name="boml",
    version="0.1.0",
    author="Yaohua Liu, Risheng Liu",
    author_email="liuyaohua@mail.dlut.edu.cn",
    description="A Bilevel Optimizer Library in Python for Meta Learning",
    long_description = long_description,
    packages=setuptools.find_packages(),
    url="https://github.com/dut-media-lab/BOML",
    license="MIT",
    install_requires=get_install_requirements(),
)
