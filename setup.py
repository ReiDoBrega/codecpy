from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codecpy",
    version="0.1.2",
    author="ReiDoBrega",
    author_email="pedro94782079@gmail.com",
    description="A comprehensive Python library for codec identification, normalization and media format analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReiDoBrega/codecpy",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "typing-extensions>=3.7.4;python_version<'3.8'",
        "dataclasses>=0.6;python_version<'3.7'",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Graphics",
    ],
    keywords=[
        "codec", "media", "video", "audio", "format", "container", "mime-type", 
        "h264", "h265", "aac", "mp4", "webm", "matroska", "mkv", "hls", "dash"
    ],
    project_urls={
        "Homepage": "https://github.com/ReiDoBrega/codecpy",
        "Repository": "https://github.com/ReiDoBrega/codecpy",
        "Bug Tracker": "https://github.com/ReiDoBrega/codecpy/issues",
    },
)