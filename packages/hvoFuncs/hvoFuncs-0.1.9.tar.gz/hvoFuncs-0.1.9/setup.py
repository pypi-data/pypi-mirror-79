import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hvoFuncs", # Replace with your own username
    version="0.1.9",
    author="Harrison Van Oort",
    author_email="harroort@amazon.com",
    description="Common functions for dataframe manipulation and for using certain applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas==0.25.3',
        'requests==2.22.0',
        'requests-ntlm==1.1.0',
        's3fs==0.4.0'
    ],
    python_requires='>=3.6',
)
