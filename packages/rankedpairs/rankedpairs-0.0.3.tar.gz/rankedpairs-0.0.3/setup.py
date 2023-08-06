import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rankedpairs", # Replace with your own username
    version="0.0.3",
    author="Simon Lequar",
    author_email="simon.lequar@gmail.com",
	license='MIT',
	keywords='voting',

    description="A lightweight ranked pairs python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sjlequar/PyRP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
