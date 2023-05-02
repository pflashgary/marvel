#!/usr/bin/env python3

import os
import coloredlogs
from dotenv import load_dotenv
from tabulate import tabulate

from lib import *

def main():
    coloredlogs.install(level='DEBUG')
    load_dotenv()

    marvel_api_public_key = os.getenv("MARVEL_API_PUBLIC_KEY")
    if marvel_api_public_key == None:
        logging.critical("MARVEL_API_PUBLIC_KEY is not set")
        quit()
    marvel_api_private_key = os.getenv("MARVEL_API_PRIVATE_KEY")
    if marvel_api_private_key == None:
        logging.critical("MARVEL_API_PRIVATE_KEY is not set")
        quit()

    logging.info(f"loaded public and private key from environment variables")

    service = MarvelService(marvel_api_public_key, marvel_api_private_key)

    characters = service.get_characters()

    character_to_comics_count = lambda character: {"name": character["name"], "comics_count": character["comics"]["available"]}
    characters_to_comic_count = map(character_to_comics_count, characters)
    sorted_characters_to_comic_count = sorted(characters_to_comic_count, key = lambda x: x["comics_count"], reverse = True)

    print(tabulate(sorted_characters_to_comic_count))



if __name__ == '__main__':
    main()
