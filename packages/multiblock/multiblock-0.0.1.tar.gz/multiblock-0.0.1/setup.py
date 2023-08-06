from setuptools import find_packages, setup

import versioneer

with open("README.rst", "r") as f:
    long_desc = f.read()

setup(
    name="multiblock",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Matt Molyneaux",
    author_email="moggers87+git@moggers87.co.uk",
    description="Sync block and mute lists over multiple Mastodon accounts",
    long_description=long_desc,
    url="https://github.com/moggers87/multiblock",
    download_url="https://pypi.org/project/multiblock/",
    packages=find_packages(),
    license="GPLv3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "click",
    ],
    extras_require={
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinx-click",
        ],
    },
    entry_points={
        "console_scripts": [
            "multiblock = multiblock.command:multiblock",
        ]
    },
)
