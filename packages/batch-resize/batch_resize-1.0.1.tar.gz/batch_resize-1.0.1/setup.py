import setuptools

setuptools.setup(
    name="batch_resize",
    version="1.0.1",
    license='MIT',
    author="YoungjuneKwon",
    author_email="shining@uvas.kr",
    description="Resize and crop all images stored in the folder.",
    long_description="""
By designating a specific folder, resize and crop all images in the sub folders of the specified folder according to settings that you specify. Also save them in the other or the originally designated folder as you specified.
    """,
    url="https://github.com/YoungjuneKwon/python-batch-resize",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)