import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botframe",  # Replace with your own username
    version="0.0.Alpha4",
    author="Eugene-Rybin",
    author_email="z.ribin20@gmail.com",
    description="Bot framework for Vk.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Waika28/botframe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "vk-api>=11.8.0"
    ],
    python_requires='>=3.6',
)
