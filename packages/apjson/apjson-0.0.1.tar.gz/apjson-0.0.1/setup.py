from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name="apjson",
    version="0.0.1",

    author="nect",
    description="A simple asynchronus json prettifier.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT License",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Natural Language :: English",
        "Intended Audience :: Developers"
    ],
    keywords="prettifier json async decorator light",


    packages=find_packages(),
    python_requires=">=3.5, <4",
    extras_require={
        "dev": ["check-manifest"]
    }
)