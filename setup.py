from setuptools import setup, find_packages

setup(
    name="code4swipe",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "code4swipe=code4swipe.code4swipe:main",
        ],
    },
    author="Andrey Danilov",
    author_email="danand@inbox.ru",
    description="A CLI tool to motivate coding by triggering a 'swipe up' via ADB when new git diff lines are detected.",
    url="https://github.com/Danand/code4swipe",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
