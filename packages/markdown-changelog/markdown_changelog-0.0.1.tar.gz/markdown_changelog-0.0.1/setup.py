from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Python-Markdown extension for easy changelog tagging"

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

PACKAGE_NAME = "markdown_changelog"
MAINTAINER = "Lukasz G. Migas"
MAINTAINER_EMAIL = "lukas.migas@yahoo.com"
URL = "https://github.com/lukasz-migas/markdown-changelog"
LICENSE = "MIT"
DOWNLOAD_URL = "https://github.com/lukasz-migas/markdown-changelog"
INSTALL_REQUIRES = ["markdown"]
PACKAGES = [package for package in find_packages()]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Text Processing :: Filters",
    "Topic :: Text Processing :: Markup :: HTML",
]
KEYWORDS = ["text", "filter", "markdown", "html", "changelog"]

setup(
    name=PACKAGE_NAME,
    author=MAINTAINER,
    author_email=MAINTAINER_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    package_dir={"markdown_changelog": "markdown_changelog"},
    entry_points={"markdown.extensions": ["changelog = markdown_changelog:ChangelogExtension"]},
)
