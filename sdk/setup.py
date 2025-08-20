"""
Setup script for XReason SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xreason-sdk",
    version="1.0.0",
    author="XReason Team",
    author_email="support@xreason.ai",
    description="Python SDK for XReason Reasoning as a Service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xreason/xreason-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.24.0",
        "pydantic>=1.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    keywords="reasoning, ai, legal, scientific, compliance, validation",
    project_urls={
        "Bug Reports": "https://github.com/xreason/xreason-sdk/issues",
        "Source": "https://github.com/xreason/xreason-sdk",
        "Documentation": "https://xreason-sdk.readthedocs.io/",
    },
)
