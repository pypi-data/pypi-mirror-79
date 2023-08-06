import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DB_helper", # Replace with your own username
    version="1.1.0",
    author="lioppp",
    author_email="stroganov400@gmail.com",
    description="Модуль для простого использования БД Sqlite3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)