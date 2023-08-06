from setuptools import setup
from setuptools import find_packages

version = "1.1.0"

install_requires = [
    "acme>=0.29.0",
    "certbot>=0.34.0",
    "setuptools",
    "mock",
    "transip",
]

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setup(
    name="certbot-dns-transip-simple",
    version=version,
    description="transip DNS Authenticator plugin for Certbot, simple to set up, no docker etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitea.caret.be/jens/certbot-dns-transip",
    author="Jens Timmerman",
    author_email="certbotdnstransip@caret.be",
    license="Apache License 2.0",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Security",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-transip = certbot_dns_transip.dns_transip:Authenticator"
        ]
    },
    test_suite="certbot_dns_transip",
)
