import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyimageexport",
    version="1.0.0",
    author="Alvaro Azael Rodriguez Rodriguez",
    author_email="azael.rguez96@gmail.com",
    description="Package to convert various formats of raster graphics images in a single line of code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/azael_rguez/py-image-export",
    packages=setuptools.find_packages(),
    install_requires=['Pillow',],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
