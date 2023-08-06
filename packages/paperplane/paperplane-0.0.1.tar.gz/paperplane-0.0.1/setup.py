from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="paperplane",
    version="0.0.1",
    author="Abhilash Kishore",
    author_email="abhilash1in@gmail.com",
    description="Paperplane",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhilash1in/paperplane",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'paperplane=paperplane:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
