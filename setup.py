from setuptools import setup, find_packages

setup(name="netdot-client",
    version="0.1",
    description="Client for the netdot rest API",
    long_description="",
    url="https://github.com/frgray/netdot-client-python",
    license='?',
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
    keywords='netdot',
    author="Francisco Gray",
    author_email="frgray@uoregon.edu",
    packages=find_packages(),
    install_requires=[
        "requests>=1.0",
    ],
)
