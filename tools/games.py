import json

from llama_index.core.tools import FunctionTool

with open("data/games.json", encoding="utf-8") as file:
    games = json.load(file)


def find_games(
    players: int,
    max_time: int,
    style: str | None = None,
    complexity: str | None = None,
) -> dict:
    """Find board games suitable for the number of players, available time, and game style."""

    if players <= 0:
        return {
            "status": "invalid_input",
            "message": "Number of players must be greater than 0.",
            "games": [],
        }

    if max_time <= 0:
        return {
            "status": "invalid_input",
            "message": "Maximum play time must be greater than 0.",
            "games": [],
        }

    valid_styles = {game["style"].lower() for game in games}

    if style is not None and style.lower() not in valid_styles:
        return {
            "status": "invalid_input",
            "message": f"Unknown style '{style}'. Available styles: {sorted(valid_styles)}.",
            "games": [],
        }

    valid_complexities = {
        game["complexity"].lower()
        for game in games
    }

    if complexity is not None and complexity.lower() not in valid_complexities:
        return {
            "status": "invalid_input",
            "message": (
                f"Unknown complexity '{complexity}'. "
                f"Available complexities: {sorted(valid_complexities)}."
            ),
            "games": [],
        }

    matches = [
        game
        for game in games
        if game["min_players"] <= players <= game["max_players"]
           and game["time"] <= max_time
           and (style is None or game["style"].lower() == style.lower())
           and (
                   complexity is None
                   or game["complexity"].lower() == complexity.lower()
           )
    ]

    if not matches:
        return {
            "status": "no_match",
            "message": "No games matching these criteria were found in the current catalog.",
            "games": [],
        }

    return {
        "status": "success",
        "games": matches,
    }

def get_game_details(game_name: str) -> dict:
    """Get details for a specific board game."""
    for game in games:
        if game["name"].lower() == game_name.lower():
            return game

    return {"error": "Game not found"}

find_games_tool = FunctionTool.from_defaults(fn=find_games)
get_game_details_tool = FunctionTool.from_defaults(fn=get_game_details)
