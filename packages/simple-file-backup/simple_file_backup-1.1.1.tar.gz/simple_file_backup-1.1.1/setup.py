import setuptools

import simple_file_backup

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="simple_file_backup",
    version=simple_file_backup.__version__,
    author="Zsolt Nagy",
    author_email="nazsolti@outlook.com",
    description="Console application for periodically backing up a single file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["simple-file-backup=simple_file_backup:cmdline"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    python_requires=">=3.8",
)
