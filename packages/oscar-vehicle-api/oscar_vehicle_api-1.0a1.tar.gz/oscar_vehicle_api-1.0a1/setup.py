import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oscar_vehicle_api",
    version="1.0a1",
    author="Nikolay Dema",
    author_email="ndema2301@gmail.com",
    description="OSCAR Vehicle API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/starline/oscar_vehicle_api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6',
)
