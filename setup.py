from setuptools import setup

setup(
    name='Shosetsu',
    version='1.1.0',
    packages=['Shosetsu'],
    url='https://github.com/ccubed/Shosetsu',
    license='MIT',
    author='Cooper Click',
    author_email='ccubed.techno@gmail.com',
    description='Python 3 Aiohttp VNDB Scraper',
    long_description='Shosetsu is a Python 3 Asyncio VNDB Website scraper that foregos the awful TCP based SQL database wrapper called an API.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries'
    ],
    keywords="VNDB asyncio aiohttp scraping",
    install_requires=['lxml', 'aiohttp', 'bs4'],

)
