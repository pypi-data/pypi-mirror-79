import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wedge-lib",
    install_requires=[
        "django",
        "var-dump",
        "arrow",
        "django-extensions",
        "serpy",
        "validators",
        "pyyaml",
        "openpyxl",
        "weasyprint",
        "djangorestframework-simplejwt",
    ],
    version="1.0.1",
    author="Wedge",
    author_email="bertrand.begouin@wedge-digital.com",
    description="A Django app to conduct and test REST API based projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.wedge-digital.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
