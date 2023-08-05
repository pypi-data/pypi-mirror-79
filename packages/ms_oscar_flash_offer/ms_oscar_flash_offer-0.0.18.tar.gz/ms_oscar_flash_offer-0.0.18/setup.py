import setuptools


try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except Exception:
    long_description = ""


setuptools.setup(
    name="ms_oscar_flash_offer",
    version="0.0.18",
    author="Making Science",
    author_email="makingscience@makingscience.com",
    description="Django oscar module to create flash offer",
    url="https://bitbucket.org/jojomakingscience/ms_oscar_flash_offer/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "django>=2.1",
        "django-oscar>=1.6",
    ],
    package_data={
        "": ["*.html"],
    },
    include_package_data=True,
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
