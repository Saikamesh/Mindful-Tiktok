from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
]

setup(
    name='tt_crawl',
    version='0.0.2',
    description='A TikTok crawler',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Saikamesh/Mindful-Tiktok',
    author='Sai Dwibhashyam',
    License='GPL-3.0 License',
    classifiers=classifiers,
    keywords='TikTok, TikTok Research API, TikTok Data',
    packages=find_packages(),
    install_requires=['requests', 'pandas'],
    python_requires='>=3.10'
)