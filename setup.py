from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Melody_CLI',
    version='0.0.2',
    description='A command-line music player that downloads and plays music from YouTube.',
    author= 'Hardik Jaiswal',
    url = 'https://github.com/pythonicforge/melody.CLI',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=setuptools.find_packages(),
    keywords=['music player python', 'music player cli', 'melody-cli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    py_modules=['Melody_CLI'],
    package_dir={'':'src'},
    install_requires = [
        'pygame',
        'yt_dlp',
        'ytmusicapi'
    ]
)
