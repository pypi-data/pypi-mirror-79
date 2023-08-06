[![Build Status](https://travis-ci.com/partojkander/hotel-names.svg?branch=master)](https://travis-ci.com/partojkander/hotel-names)

# hotel-names
Generate hotel names

Heavily inspired by https://github.com/treyhunner/names
## Usage

When installed, you can use it from command line:

    $ hotel_names
    Urban Mountains Inn

To use as a package:

    >>> from hotel_names import hotel_names
    >>> hotel_names.get_hotel_name()
    'Fancy Sea Hotel'
    >>> hotel_names.get_hotel_name(suffix="by the sea")
    'Happy Beach by the sea'

## License

This project is released under an MIT License.