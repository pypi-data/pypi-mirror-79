import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fasta_manipulate",
    version="2.0.0",
    author="Wilson",
    author_email="3120195705@bit.edu.cn",
    url="https://github.com/WeiSong-bio/fasta_manipulate",
    description="fasta-manipulate is used to merge multiple line sequences in fasta files into one line sequence and count the number of different length sequences in the fasta file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'fasta_manipulate=fasta_manipulate.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
         # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
    ],
)
