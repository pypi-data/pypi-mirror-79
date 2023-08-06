from distutils.core import setup

setup(
    name = "pycryptometer",
    version = "1.0.0",
    license = "MIT",
    author = "ToasterUwU",
    description = "API Wrapper for cryptometer.io",
    url = "https://github.com/ToasterUwU/pycryptometer",
    keywords = ['API', 'Cryptometer'],
    install_requires=[
        'requests',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)