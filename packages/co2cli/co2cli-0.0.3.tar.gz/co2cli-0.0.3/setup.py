import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="co2cli", # Replace with your own username
    version="0.0.3",
    scripts=["co2cli/co2cli"],
    author="Piyush Dongre",
    author_email="piyush.dongre@yahoo.com",
    description="A package to calculate the CO2 emissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PiyushD17/CO2-CLI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'click==7.1.2',
      ],
    python_requires='>=3.5',
)
