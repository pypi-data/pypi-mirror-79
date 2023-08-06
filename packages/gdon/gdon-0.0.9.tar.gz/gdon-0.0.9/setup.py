import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdon",
    version="0.0.9",
    author="matograine",
    author_email="matograine@zaclys.net",
    description="gdon helps creating paper tips for the Ğ1 libre crypto-currency ; and retrieve them after expiry.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://git.duniter.org/matograine/g1pourboire/-/tags/0.0.9",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: French",
    ],
    python_requires='>=3.6',
    install_requires=[
        # Silkaj packages
        "duniterpy==0.56",
        "ipaddress",
        "texttable",
        "tabulate",
        "pynacl",
        # G1don specific packages
        "Pillow>=6.0.0",
        "qrcode>=6.1",
        "reportlab>=3.5.23",
    ],
    scripts=["bin/gdon"],
)

