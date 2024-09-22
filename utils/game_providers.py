import json
from abc import ABC, abstractmethod

import requests
from enum import Enum


class GameProvider(ABC):
  """
  GameProvider is an abstract base class that defines the interface for game providers.
  Attributes:
    api_link (str): The API endpoint to fetch game data.
    download_type (str): The type of download method, either 'torrent' or 'direct'.
    logo (str, optional): The logo of the game provider.
  Methods:
    __init__(self, api_link, download_type, logo=None):
      Initializes the GameProvider with the given API link, download type, and optional logo.
    get_game_list(self):
      Abstract method that should be implemented by subclasses to return a list of games.
    fetch_json_data(self):
      Fetches JSON data from the API link. Raises an HTTPError if the request fails.
    get_download_type(self):
      Returns the download type.
    get_logo(self):
      Returns the logo of the game provider.
  """

  def __init__(self, api_link, download_type, logo=None):
    self.api_link = api_link
    self.download_type = download_type  # This can be set to 'torrent' or 'direct' by subclasses or other methods
    self.logo = logo

  @abstractmethod
  def get_game_list(self):
    pass

  def fetch_json_data(self):
    response = requests.get(self.api_link, headers={"Accept": "application/json"})
    if response.status_code == 200:
      return response.json()
    else:
      response.raise_for_status()
  
  def get_download_type(self):
    return self.download_type
  
  def get_logo(self):
    return self.logo
      
class SteamRipProvider(GameProvider):
  def __init__(self):
    super().__init__("https://hydralinks.cloud/sources/steamrip.json", "direct", "https://i.imgur.com/Ok00lU7.png")
    
  def get_game_list(self):
    json_data = super().fetch_json_data()
    return json_data.get("downloads", [])
  
class FitGirlProvider(GameProvider):
  def __init__(self):
    super().__init__("https://hydralinks.cloud/sources/fitgirl.json", "torrent", "https://i.imgur.com/RZUbMYs.png")
    
  def get_game_list(self):
    json_data = super().fetch_json_data()
    return json_data.get("downloads", [])
