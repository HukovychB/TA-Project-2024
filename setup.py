from setuptools import setup


setup(
    name="TA Project 2024",
    version="0.1",
    description="Web application for applying technical analysis on financial instruments",
    author="Bohdan Hukovych & Jaroslav Louda",
    author_email="72617770@fsv.cuni.cz & 45673694@fsv.cuni.cz",
    url="https://github.com/HukovychB/TA-Project-2024",
    packages=find_packages(where="app"),
    long_description=open('README.md').read(),
    install_requires=["numpy", 
                      "pandas",
                      ],
)