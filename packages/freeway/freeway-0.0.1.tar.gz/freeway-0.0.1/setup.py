from setuptools import setup

with open('README.md', 'r') as desc:
    long_description = desc.read()
    

setup(
    name="freeway",
    version='0.0.1',
    license='MIT',
    packages=["freeway"],
    description="Freeway is a module for managing file system structures with recursive pattern rules.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cesioarg",
    download_url = 'https://github.com/cesioarg/freeway/archive/v1.0.0.tar.gz',
    author="Leandro Inocencio",
    author_email="cesio.arg@gmail.com",
    keywords = ['filesystem', 'pipeline', 'parser', 'forder', 'patternvideos'],
    package_dir={'':'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Filesystems",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            ]
    }
)
