import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tagore",
    version="1.1.0",
    author="Applied Bioinformatics Laboratory",
    author_email="abil@ihrc.com",
    description="A simple way to visualize features on human chromosome ideograms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jordanlab/tagore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Scientific/Engineering :: Visualization"
    ],
    python_requires='>=3.6',
    install_requires=['click'],
    keywords = ['Human', 'chromosome', 'ideogram', 'visualization'],
    scripts = ['tagore', 'scripts/rfmix2tagore.py'],
    data_files = [('lib/tagore-data/', ['base.svg.p'])]
)