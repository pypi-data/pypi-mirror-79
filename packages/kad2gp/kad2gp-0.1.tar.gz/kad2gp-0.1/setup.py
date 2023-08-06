import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='kad2gp',
    version='0.1',
    author="Anton Serebryakov",
    author_email="serebryakov.anton@gmail.com",
    description="Converts http://pkk.rosreestr.ru to Garden Planner's file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TonSilver/kad2gp",
    packages=['kad2gp'],
    entry_points={
        'console_scripts': [
            'kad2gp=kad2gp.main_converter:main',
        ],
    },
    install_requires=[
        'rosreestr2coord',
        'opencv-python',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
)
