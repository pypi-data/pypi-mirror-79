import setuptools

setuptools.setup(
    name="vedicpy", 
    version="0.0.7",
    author="Utkarsh Mishra",
    author_email="utkarsh.um07@gmail.com",
    description="A Python Package for Vedic Mathematics",
    long_description_content_type="text/markdown",
    url="https://github.com/utkarsh0702/vedicpy",
    packages=setuptools.find_packages(exclude=['tests*']),
    test_suite='tests',
    license="BSD",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    keyword="vedic python",
    python_requires='>=3.6',
)

