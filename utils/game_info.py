import json
import re

import requests
from igdb.wrapper import IGDBWrapper

from backend import igdb_client_id, igdb_client_secret, log
from utils.game_providers import GameProvider


async def retrieve_game_links(game_name: str, provider: GameProvider) -> dict:
    """
    Asynchronously retrieves game links based on the provided game name and game provider.
    Args:
        game_name (str): The name of the game to search for.
        provider (GameProvider): An instance of GameProvider to retrieve the game list from.
    Returns:
        dict: A dictionary containing the found games with their titles and stripped titles if any matches are found.
        None: If no games match the provided game name.
    """

    game_list = provider.get_game_list()

    found_games = []

    for game in game_list:
        stripped_title = strip_game_title(game.get("title", ""))

        title = game.get("title", "").lower()
        if game_name.lower() in title:
            game.update({"stripped_title": stripped_title})
            game.update({"download_type": provider.get_download_type()})
            game.update({"provider_logo": provider.get_logo()})
            found_games.append(game)

    if found_games:
        return found_games
    return None


def retrieve_game_details(game_name: str):
    """
    Retrieve detailed information about a game from the IGDB API and Steam.
    Args:
        game_name (str): The name of the game to retrieve details for.
    Returns:
        dict: A dictionary containing the game's cover image, summary, total rating, 
              and a header image URL from Steam.
    Raises:
        Exception: If there is an issue with the API requests or data parsing.
    """
    wrapper = IGDBWrapper(igdb_client_id, get_token())

    game_byte_array = wrapper.api_request(
        "games", f'search "{game_name}"; fields cover,summary,total_rating; limit 1;'
    )
    game_byte_decoded = game_byte_array.decode("utf-8")
    game_details = json.loads(game_byte_decoded)[0]

    steam_app_id_byte = wrapper.api_request(
        "external_games", f'fields uid; where category = 1 & game = {game_details["id"]}; limit 1;'
    )
    steam_app_id_decoded = steam_app_id_byte.decode("utf-8")
    steam_app_id = json.loads(steam_app_id_decoded)
    
    header = f"https://cdn.akamai.steamstatic.com/steam/apps/{steam_app_id[0]["uid"]}/header.jpg"
    
    game_details.update({"header": header})
    return game_details

def get_token():
    """
    Fetches an OAuth2 access token from Twitch.

    This function sends a POST request to the Twitch OAuth2 token endpoint
    with the client ID, client secret, and grant type as parameters. It
    returns the access token if the request is successful.

    Returns:
        str: The access token if the request is successful, otherwise None.
    """
    r = requests.post(
        "https://id.twitch.tv/oauth2/token",
        params={
            "client_id": igdb_client_id,
            "client_secret": igdb_client_secret,
            "grant_type": "client_credentials",
        },
    )
    return json.loads(r.text).get("access_token", None)

def strip_game_title(title: str) -> str:
    """
    Strips unnecessary parts from a game title.
    This function removes specific keywords such as "Free Download" and "Build" 
    from the title. Additionally, it uses a regular expression to remove any 
    version numbers that start with a number followed by dots and digits.
    Args:
        title (str): The original game title.
    Returns:
        str: The cleaned game title.
    """
    # Split the title based on specific keywords
    for keyword in ["Free Download", "Build"]:
        title = title.split(keyword, 1)[0].strip()

    # Use regex to split if the pattern starts with a number followed by dots and digits
    title = re.split(r'\b\d+(?:\.\d+)+\b', title, 1)[0].strip()

    return title
