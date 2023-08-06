from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="easy_env_var",
    version="1.0.1",
    author="Geekeno",
    author_email="dev@geekeno.com",
    description="Simple util to get environment variables in the right data type.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.geekeno.com/utils/easy-env",
    packages=find_packages(exclude=["*.tests*"]),
    zip_safe=True,
    tests_require=["tox", "coverage[toml]"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://gitlab.geekeno.com/utils/easy-env",
        "Source": "https://gitlab.geekeno.com/utils/easy-env",
        "Tracker": "https://gitlab.geekeno.com/utils/easy-env/-/issues",
    },
)
