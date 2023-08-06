import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplebeep",
    version="0.0.1",
    author="Leberwurscht",
    author_email="leberwurscht@hoegners.de",
    description="Platform-independent beep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/leberwurscht/simplebeep",
    packages=setuptools.find_packages(),
    install_requires=[
        "simpleaudio; sys_platform == 'darwin' or sys_platform == 'win32'",
        'numpy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
