import setuptools


setuptools.setup(
    name="fixedrobo",
    version="1.2",
    author="noidea",
    author_email="",
    description="Fixed version of robobrowser",

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4>=4.3.2',
        'requests>=2.6.0',
        'six>=1.9.0',
        'Werkzeug>=0.10.4',
    ],
    python_requires='>=3.6',
)