"""Utility Helper Functions"""
import math
import pandas as pd
from typeguard import typechecked


@typechecked
def go_group(num: float) -> str:
    """Puts go_boost into groups from Ben Baldwin"""
    if num > 4:
        return "definitely_go"
    elif num > 1:
        return "probably_go"
    elif num > -1:
        return "toss_up"
    elif num > -4:
        return "probably_kick"
    else:
        return "definitely_kick"


@typechecked
def mean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Take average values for each team/season"""
    mdf = (
        df[["team_season", "go", "go_boost", "agree", "season"]]
        .groupby(["team_season"])
        .mean()
    )
    mdf["season"] = mdf["season"].astype(int)
    mdf["team"] = [x.split("__")[0] for x in mdf.index]
    return mdf


# from https://codereview.stackexchange.com/questions/41298/producing-ordinal-numbers
@typechecked
def ordinal(num: int) -> str:
    """Returns Oridinal Name for Numbers"""
    SUFFIXES = {1: "st", 2: "nd", 3: "rd"}
    if 10 <= num % 100 <= 20:
        suffix = "th"
    else:
        # the second parameter is a default.
        suffix = SUFFIXES.get(num % 10, "th")
    return str(num) + suffix


def play_summary(
    play: pd.DataFrame, baseteam: str = "TEN", stat: str = "wp", astat: str = "wpa"
) -> str:
    """Returns String Summary of Play Description
    Parameters
    ----------

    play: pd.DataFrame
        pandas dataframe containing one row of a play to summarize
    baseteam: str
        team of interest
    stat: str
        base statistic to consider (WP or EP)
    astat: str
        additive statistic to consider (WPA or EPA)
    """

    assert play.shape[0] == 1, "Must be dataframe of a single row"

    time = play["time"].values[0]
    yrdln = play["yrdln"].values[0]
    togo = int(play["ydstogo"].values[0])
    qtr = int(play["qtr"])
    season = int(play["season"])
    week = int(play["week"])
    if qtr == 5:
        qtr = "OT"
    else:
        qtr = ordinal(int(qtr)) + " Quarter"

    down = ordinal(int(play["down"]))

    hometeam = play["home_team"].values[0]
    awayteam = play["away_team"].values[0]

    homescore = int(play["total_home_score"].values[0])
    awayscore = int(play["total_away_score"].values[0])

    ## subtract TD because it's included if they score and I want starting situation
    if play["touchdown"].values[0] == 1:
        tdteam = play["td_team"].values[0]
        if tdteam == hometeam:
            homescore = homescore - 6
        else:
            awayscore = awayscore - 6

    stat_val = round(play[stat].values[0], 2)
    astat_val = round(play[astat].values[0], 2)
    nstat_val = round(stat_val + astat_val, 2)

    sentence = f"{season} (week {week}): {awayteam} ({awayscore}) at {hometeam} ({homescore}). {time} left in {qtr}. {down} down and {togo} at {yrdln}. {stat.upper()}: {str(stat_val)} -> {str(nstat_val)}"
    return sentence


@typechecked
def roundboost(num: float) -> int:
    """Rounds Positive Numbers Up and Negative Numbers Down"""
    if num >= 0:
        return math.ceil(num)
    elif num < 0:
        return math.floor(num)
