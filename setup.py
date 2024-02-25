from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3",
]

setup(
    name="tt_crawl",
    version="0.0.28",
    description="A Python package for interacting with TikTok Research API",
    long_description=open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Saikamesh/Mindful-Tiktok",
    author="Sai Dwibhashyam",
    license="GPL-3.0 License",
    classifiers=classifiers,
    keywords="TikTok, TikTok Research API, TikTok API, TikTok Data",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=["requests==2.31.0", "pandas==2.1.4"],
)
