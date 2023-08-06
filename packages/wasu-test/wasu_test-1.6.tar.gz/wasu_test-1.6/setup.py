import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wasu_test",
    version="1.6",
    author="XiaoDong Chen",
    author_email="chenxiaodong@wasu.com",
    description="The Wasu Auto TestFrameWork",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['PyYAML>=5.3', 'PyMySql>=0.10.1',
                      'xlrd>=1.2.0', 'requests==2.24.0'
                      'selenium==3.11.0','python_benedict==0.19.0'
                      ],
    entry_points={

    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
