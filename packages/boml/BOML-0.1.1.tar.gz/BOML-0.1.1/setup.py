from setuptools import setup,find_packages
from os import path

current_directory = path.abspath(path.dirname(__file__))


def get_install_requirements():
    requirements_path = path.join(current_directory, "requirements.txt")
    with open(requirements_path, encoding="utf-8") as fp:
        return fp.read().splitlines()


setup(
    name="BOML",
    version="0.1.1",
    packages=find_packages(),
    url="https://github.com/dut-media-lab/BOML",
    license="MIT",
    keywords=[
    "meta-learning",
    "bilevel-optimization",
    "few-shot-lerning",
    "python",
    "Deep learning"],
    install_requires=get_install_requirements(),
    classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=3.5,<3.8',
    author="Yaohua Liu, Risheng Liu",
    author_email="liuyaohua@mail.dlut.edu.cn",
    description="A Bilevel Optimizer Library in Python for Meta Learning",
)
