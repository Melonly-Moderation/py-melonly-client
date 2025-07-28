from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="melonly-api",
    version="1.0.0",
    author="Melonly API Client",
    author_email="admin@melonly.xyz",
    description="A Python client library for the Melonly API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Melonly-Moderation/py-melonly-client",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp",
        "urllib3",
        'typing-extensions>=4.0.0;python_version<"3.8"',
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    keywords="melonly api client discord server management",
    project_urls={
        "Bug Reports": "https://github.com/Melonly-Moderation/py-melonly-client/issues",
        "Source": "https://github.com/Melonly-Moderation/py-melonly-client",
    },
)