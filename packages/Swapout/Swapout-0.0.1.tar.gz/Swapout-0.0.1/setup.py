import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Swapout",
    version="0.0.1",
    author="Shanfeng Hu",
    author_email="shanfeng.hu1991@gmail.com",
    description="Swapout: Exchanging Pixels for Long-range Spatial Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shanfenghu/Swapout",
    py_modules=["Swapout"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
