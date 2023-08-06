import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="direct-debit",
    version="0.0.0",
    author="direct debit",
    author_email="arie@directdebit.co.za",
    description="A wrapper around Direct Debit's debit order collection API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://directdebit.co.za",
    project_urls={
        "Source Code": "https://github.com/Direct-Debit/direct-debit-python-client",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
