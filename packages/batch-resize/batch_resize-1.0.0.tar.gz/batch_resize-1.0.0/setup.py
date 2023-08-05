import setuptools

setuptools.setup(
    name="batch_resize",
    version="1.0.0",
    license='MIT',
    author="YoungjuneKwon",
    author_email="shining@uvas.kr",
    description="Resize and crop all images stored in the folder.",
    long_description=open('README.md').read(),
    url="https://github.com/YoungjuneKwon/python-batch-resize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)