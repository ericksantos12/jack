import json
import requests
from backend import log, igdb_client_id, igdb_client_secret
from igdb.wrapper import IGDBWrapper
import re


async def retrieve_game_links(game_name) -> dict:
    r = requests.get(
        f"https://hydralinks.cloud/sources/steamrip.json",
        headers={"Accept": "application/json"},
    )
    json_data = json.loads(r.text)
    downloads = json_data.get("downloads", [])

    found_games = []

    for game in downloads:
        stripped_title = strip_game_title(game.get("title", ""))

        title = game.get("title", "").lower()
        if game_name.lower() in title:
            game.update({"stripped_title": stripped_title})
            found_games.append(game)

    if found_games:
        return found_games
    return None


def retrieve_game_details(game_name: str):
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
    # Split the title based on specific keywords or a pattern that starts with a number
    for keyword in ["Free Download", "Build"]:
        title = title.split(keyword, 1)[0].strip()

    # Use regex to split if the pattern starts with a number followed by dots and digits
    title = re.split(r'\b\d+(?:\.\d+)+\b', title, 1)[0].strip()

    return title
