from random import choice


adjectives = ["Beautiful", "Fancy", "Happy", "Imperial", "Quiet", "Rosy", "Spring", "Sunny", "Urban"]
nouns = ["Beach", "Downs", "Gardens", "Hills", "Lake", "Mountains", "Sea"]
suffixes = ["B&B", "Club", "Hotel", "Inn", "Resorts", "Spa", "Suites", "Tower"]


def get_hotel_name(adjective=None, noun=None, suffix=None):
    adjective_ = adjective or choice(adjectives)
    noun_ = noun or choice(nouns)
    suffix_ = suffix or choice(suffixes)
    return f"{adjective_} {noun_} {suffix_}"


def main():
    print(get_hotel_name())


if __name__ == '__main__':
    main()
