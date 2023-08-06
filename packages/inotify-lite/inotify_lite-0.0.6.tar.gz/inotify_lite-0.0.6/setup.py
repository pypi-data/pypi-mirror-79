import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
        name="inotify_lite",
        version="0.0.6",
        author="Joshua Munn",
        author_email="public@elysee-munn.family",
        description="Linux inotify wrapper",
        long_description=long_description,
        long_description_content_type="text/x-rst",
        url="https://github.com/jams2/inotify_lite",
        packages=setuptools.find_packages(),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            "Operating System :: POSIX :: Linux",
        ],
        python_requires=">=3.6",
        extras_require={
            "dev": ["pytest", "pytest-mypy", "pytest-flake8"],
            "dist": ["setuptools", "wheel", "twine"],
            "docs": ["sphinx"],
        },
    )
