import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="publish-test-8368822371",
    version="0.0.3",
    packages=setuptools.find_packages(),

    # Meta data
    author="Kok Tsz Ho Zelca",
    author_email="zelcakok@outlook.com",
    description="A framework for building microservices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/koktszhozelca/pycube",
    project_urls={
        "Bug Tracker": "https://gitlab.com/koktszhozelca/pycube/-/issues",
        "Source Code": "https://gitlab.com/koktszhozelca/pycube"
    },
    install_requires=[
        "aiohttp==3.6.2",
        "async-timeout==3.0.1",
        "attrs==20.2.0",
        "chardet==3.0.4",
        "idna==2.10",
        "multidict==4.7.6",
        "typing-extensions==3.7.4.3",
        "yarl==1.5.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)