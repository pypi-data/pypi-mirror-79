import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="co2cli_pkg", # Replace with your own username
    version="0.0.1",
    # scripts=["co2cli_pkg/co2cli"],
    author="Piyush Dongre",
    author_email="piyush.dongre@yahoo.com",
    description="A package to calculate the CO2 emissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PiyushD17/CO2-CLI",
    packages=setuptools.find_packages(exclude=("tests",)),
    # packages=["co2cli_pkg"],
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'click==7.1.2',
      ],
      entry_points={
      "console_scripts": [
            "new=co2cli_pkg.__main__:main",
        ]
      },
    python_requires='>=3.5',
)
