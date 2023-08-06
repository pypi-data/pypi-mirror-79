import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="polynomial_regression",
    version="0.0.2",
    author="Krushnakant Bhattad",
    author_email="krushnakant@cse.iitb.ac.in",
    description="Polynomial Regression for points in X-Y Plane",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/the-krushnakant/polynomial-regression",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy'],
    python_requires='>=3.6',
)