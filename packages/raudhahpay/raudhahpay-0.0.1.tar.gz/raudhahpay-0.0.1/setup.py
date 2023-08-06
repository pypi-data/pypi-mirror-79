import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raudhahpay",
    version="0.0.1",
    author="Farid Yusof",
    author_email="faridyusof727@gmail.com",
    description="Raudhah Pay Python Simple SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/faridyusof727/raudhahpayapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
)