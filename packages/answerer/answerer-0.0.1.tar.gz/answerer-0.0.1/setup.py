from distutils.core import setup

setup(
    name="answerer",
    packages=["answerer"],
    version="0.0.1",
    license="Apache",
    description="A system that uses containers and scripts to answer issues at *high* speeds.",
    long_description="See here for more information: https://github.com/abrow425/ns-answerer/",
    author="Andrew Brown (aka SherpDaWerp)",
    author_email="abrow425@gmail.com",
    url="https://github.com/abrow425/ns-answerer/",
    download_url="https://github.com/abrow425/ns-answerer/archive/v0.0.1.tar.gz",
    keywords=["NATIONSTATES", "NS", "API"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "nspy_wrapper",
        "selenium",
    ],
)
