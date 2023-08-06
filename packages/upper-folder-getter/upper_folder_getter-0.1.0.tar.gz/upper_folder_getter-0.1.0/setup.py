import setuptools

with open("README.md","r") as f:
    long_descr = f.read()

setuptools.setup(
    name="upper_folder_getter",
    version="0.1.0",
    author="Dima B",
    description="ImportError workaround",
    long_description=long_descr,
    url="https://github.com/eonianmonk/AntiImportError",
	packages=setuptools.find_packages(),
	license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
