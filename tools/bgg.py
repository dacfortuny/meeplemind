import os
import xml.etree.ElementTree as ET

import requests
from dotenv import load_dotenv
from llama_index.core.tools import FunctionTool

load_dotenv()

BGG_API_TOKEN = os.getenv("BGG_API_TOKEN")

BGG_CANDIDATES = [
    "Azul",
    "Wingspan",
    "Terraforming Mars",
    "Cascadia",
    "The Mind",
    "Just One",
    "Codenames",
]

def get_bgg_candidates() -> list[dict]:
    """Get detailed BGG information for a predefined list of candidate games."""

    games = []

    for game_name in BGG_CANDIDATES:
        game = get_bgg_game_by_name(game_name)

        if game.get("status") != "not_found":
            games.append(game)

    return games

def search_bgg_game(game_name: str) -> list[dict]:
    """Search BoardGameGeek for a board game by name."""

    url = "https://boardgamegeek.com/xmlapi2/search"

    headers = {
        "Authorization": f"Bearer {BGG_API_TOKEN}",
    }

    params = {
        "query": game_name,
        "type": "boardgame",
        "exact": 1,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    results = []

    for item in root.findall("item"):
        year_element = item.find("yearpublished")

        results.append(
            {
                "id": item.get("id"),
                "name": item.find("name").get("value"),
                "year": (
                    year_element.get("value")
                    if year_element is not None
                    else None
                ),
            }
        )

    return results

def get_bgg_game_details(game_id: str) -> dict:
    """Get detailed information for a BoardGameGeek game by ID."""

    url = "https://boardgamegeek.com/xmlapi2/thing"

    headers = {
        "Authorization": f"Bearer {BGG_API_TOKEN}",
    }

    params = {
        "id": game_id,
        "stats": 1,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)
    item = root.find("item")

    if item is None:
        return {
            "status": "not_found",
            "message": f"Game with id {game_id} was not found.",
        }

    primary_name = item.find("name[@type='primary']")
    year = item.find("yearpublished")
    min_players = item.find("minplayers")
    max_players = item.find("maxplayers")
    playing_time = item.find("playingtime")
    min_playing_time = item.find("minplaytime")
    max_playing_time = item.find("maxplaytime")
    ratings = item.find("statistics/ratings")
    average_rating = ratings.find("average") if ratings is not None else None
    average_weight = ratings.find("averageweight") if ratings is not None else None
    categories = [
        link.get("value")
        for link in item.findall("link[@type='boardgamecategory']")
    ]
    mechanics = [
        link.get("value")
        for link in item.findall("link[@type='boardgamemechanic']")
    ]

    return {
        "id": item.get("id"),
        "name": primary_name.get("value") if primary_name is not None else None,
        "year": int(year.get("value")) if year is not None else None,
        "min_players": (
            int(min_players.get("value"))
            if min_players is not None
            else None
        ),
        "max_players": (
            int(max_players.get("value"))
            if max_players is not None
            else None
        ),
        "playing_time": (
            int(playing_time.get("value"))
            if playing_time is not None
            else None
        ),
        "min_playing_time": (
            int(min_playing_time.get("value"))
            if min_playing_time is not None
            else None
        ),
        "max_playing_time": (
            int(max_playing_time.get("value"))
            if max_playing_time is not None
            else None
        ),
        "rating": (
            float(average_rating.get("value"))
            if average_rating is not None
            else None
        ),
        "complexity": (
            float(average_weight.get("value"))
            if average_weight is not None
            else None
        ),
        "categories": categories,
        "mechanics": mechanics,
    }

def get_bgg_game_by_name(game_name: str) -> dict:
    """Search BoardGameGeek for an exact game name and return its details."""

    results = search_bgg_game(game_name)

    if not results:
        return {
            "status": "not_found",
            "message": f"Game '{game_name}' was not found on BoardGameGeek.",
        }

    game_id = results[0]["id"]

    return get_bgg_game_details(game_id)

def filter_bgg_candidates(
    players: int,
    max_time: int,
    max_complexity: float | None = None,
) -> list[dict]:
    """Filter BGG candidate games by player count, maximum time, and complexity."""

    games = get_bgg_candidates()

    matches = [
        game
        for game in games
        if game["min_players"] <= players <= game["max_players"]
        and game["max_playing_time"] <= max_time
        and (
            max_complexity is None
            or game["complexity"] <= max_complexity
        )
    ]

    return matches


get_bgg_game_by_name_tool = FunctionTool.from_defaults(
    fn=get_bgg_game_by_name
)
filter_bgg_candidates_tool = FunctionTool.from_defaults(
    fn=filter_bgg_candidates
)