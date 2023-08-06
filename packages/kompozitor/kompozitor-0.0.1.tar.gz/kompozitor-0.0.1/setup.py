import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kompozitor",
    version="0.0.1",
    author="Jovan Popovic",
    author_email="jocapc@gmail.com",
    description="Biblioteka nota za komponovanje melodija",
    long_description="Biblioteka sadrzi funkcije koje predstavljaju note kojima se mogu predstaviti melodije kao Python programi.",
    long_description_content_type="text/markdown",
    url="https://github.com/jocapc/python-kompozitor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
