import setuptools
import os

os.system("export PATH=$PATH:~/.local/bin")

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kubextract",
    version="1.1.1",
    author="Bentar Dwika",
    author_email="bentar@warungpintar.co",
    description="cli framework generator for developing ML on kubeflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'kubernetes',
        'ruamel.yaml',
        'click',
        'PyInquirer',
        'requests',
        'kfp'
    ],
    entry_points={
        'console_scripts': [
            'kubextract = utils.kubextract:main',
        ],
    },
    python_requires='>=3.6',
)
