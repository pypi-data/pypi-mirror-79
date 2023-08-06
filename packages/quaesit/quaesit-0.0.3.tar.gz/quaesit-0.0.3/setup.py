import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quaesit",
    version="0.0.3",
    license="MIT",
    author="Jonas Gregorio",
    author_email="jonas.gregorio@gmail.com",
    description="Quick and easy simulation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgregoriods/quaesit.git",
    packages=setuptools.find_packages(),
    keywords=["Agent-Based Model", "Simulation"],
    install_requires=[
        "matplotlib",
        "numpy",
        "rasterio",
        "tqdm",
        "scipy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
