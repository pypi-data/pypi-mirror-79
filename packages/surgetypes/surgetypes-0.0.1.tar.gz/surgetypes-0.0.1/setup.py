
import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="surgetypes", # Replace with your own username
    version="0.0.1",
    author="Joshua p-f",
    author_email="jporrittfraser@gmail.com",
    description="Automated type checking",
    long_description="Automated type checking",
    long_description_content_type="text/markdown",
    url="https://github.com/joshp-f/surgetypes-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)