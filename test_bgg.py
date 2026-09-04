from tools.bgg import filter_bgg_candidates


games = filter_bgg_candidates(
    players=4,
    max_time=45,
    max_complexity=2.0,
)

for game in games:
    print(
        game["name"],
        game["min_players"],
        game["max_players"],
        game["max_playing_time"],
        game["complexity"],
    )