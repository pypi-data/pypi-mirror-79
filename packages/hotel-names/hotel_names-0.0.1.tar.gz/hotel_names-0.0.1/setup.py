import hotel_names
from setuptools import setup, find_packages


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGES.md') as changes_file:
    changes = changes_file.read()


setup(
    name=hotel_names.__title__,
    version=hotel_names.__version__,
    author=hotel_names.__author__,
    url="https://github.com/partojkander/hotel-names",
    description="Generate random hotel names",
    long_description='\n\n'.join((
        readme,
        changes,
    )),
    license=hotel_names.__license__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hotel_names = hotel_names.hotel_names:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='test_hotel_names',
)