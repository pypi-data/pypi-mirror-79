import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="muscle-musedev", # Replace with your own username
    version="0.0.3",
    scripts=["muscle"],
    author="MuseDev",
    author_email="support@emuse.dev",
    description="A CLI for running Muse jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/musedev/muscle",
    packages=setuptools.find_packages(),
    py_modules=["requests_helper"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
