import pastebin_python
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name=pastebin_python.__app_name__,
    version=pastebin_python.__version__,
    description=pastebin_python.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=pastebin_python.__author__,
    author_email=pastebin_python.__author_email__,
    packages=['pastebin_python', 'pastebin_python_scraper'],
    url=pastebin_python.__app_url__,
    install_requires=[
        'pymongo',
        'argparse',
        'logging',
        're',
        'time',
        'sys',
        'pprint',
        'flask',
        'bson',
        'requests'
    ],
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ),
    download_url=pastebin_python.__download_url__,
)
