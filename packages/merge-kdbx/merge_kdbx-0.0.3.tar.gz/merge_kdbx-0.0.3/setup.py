import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="merge_kdbx",
    version="0.0.3",
    author="rollman054",
    author_email="qwpmb554@gmail.com",
    description="A mergetool for Keepass 2.x databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RollMan/merge_kdbx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts':[
            'merge_kdbx = merge_kdbx.merge_kdbx:main'
        ]
    },
)