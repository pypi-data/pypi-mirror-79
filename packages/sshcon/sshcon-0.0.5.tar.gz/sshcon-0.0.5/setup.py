from setuptools import setup, find_packages
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
with open(current_dir.joinpath("VERSION")) as ver_file:
    version = ver_file.read().strip()

setup(
    name="sshcon",
    keywords=["ssh", "ssh2"],
    version=version,
    license="MIT",
    description="SSH connector for Linux systems",
    author="racoonx2p",
    author_email="racoonx2p@gmail.com",
    packages=find_packages(),
    url="https://github.com/racoonx2p/sshcon",
    download_url="https://github.com/racoonx2p/sshcon/archive/0.0.5.tar.gz",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=["ssh2-python"],
    python_requires=">=3.6",
)
