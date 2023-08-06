import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="server_uptime_app",
    version="0.0.1",
    author="Multi",
    author_email="multiidev@gmail.com",
    description="A package to keep an application online with HTTPS requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codebankco/keep-alive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)