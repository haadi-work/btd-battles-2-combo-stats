# 🎈 BTD Battles 2 — Combo Win Rate Analysis

As a university student, I do not really get the time to game anymore, but when I occasionally can, I play a game called "Bloons TD Battles 2", also known as "Battles 2". I have been a long-time fan of the Bloons TD franchise, having played BTD 5 and Battles 1 when I was younger.

In Battles 2, you are only allowed to use one hero and three towers in a match. Therefore, it becomes key that you choose towers with good synergy in order to maximise your chances of winning.

**🔗 Live app:** https://btd-battles-2-combo-stats.streamlit.app/

## Overview

This project takes a bunch of match data from HoM (top) players, and analyses that data to see which hero/monkey combos win more games.

## How It Works

This works because Ninja Kiwi (the developer of Battles 2) runs a free, official “Open Data API”. I began the project by getting my own "Open Access Key" (OAK), and using it to analyse my own recent matches. However, I am just one player (who uses the same few hero/tower combos over and over) so that was not nearly enough data to come to a proper conclusion. The key breakthrough was every match record includes the opponent’s profile link too, which I will further explain in the next section.

After gathering all this data, it was time to sort through it and pick out the relevant parts. For example, in Battles 2, it is possible to buy cosmetic skins for heroes. However, this causes the cosmetic skin to be listed as a separate hero with its own separate winrate. This was fixed by removing the skin suffix (hero.split("_")[0]) and re-aggregating on that base name. Another key issue required deduplicating matches by match ID, since the same match can be discovered twice, once from each player’s perspective.

## Interesting Challenges

The biggest "Eureka!" moment for me in this project was when I realised that I could only gather data from HoM players. Originally, the plan was to "snowball sample". I would start with the data of my matches, then for each of the opponents I played, I would take their profileURL, then get their match data, then get their opponents' data and it would continue to "snowball". However, everytime I ran the code, it would add no new data. To find the error, I tested a single profile directly and printed the response:

```
{'error': 'Invalid user ID / User is not in valid HoM', 'success': False}
```

The problem was that the players I was playing against weren't in the Hall of Masters (the top player league). Anyone who isn’t currently ranked there returns that exact error, even though their basic profile is publicly fetchable. Nothing in the API’s available documentation states this restriction up front — it only became clear by noticing that literally every failing profile was a non-HoM player.

The fix was to start the search from the HoM leaderboard. Since HoM players generally play other HoM players, this would actually add the data I needed. The added benefit was that my dataset comprised only of the top players' matches, which was perfect for seeing which heroes/monkeys would perform well even against the most skilled opponents.

## Tech Stack

- **Data collection:** Python, [Ninja Kiwi Open Data API](https://data.ninjakiwi.com)
- **Data processing:** pandas
- **Dashboard:** Streamlit + Altair
- **Hosting:** Streamlit Community Cloud

## Running It Locally

```bash
git clone https://github.com/haadi-work/btd-battles-2-combo-stats.git
cd btd-battles-2-combo-stats
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
.
├── app.py                # Streamlit dashboard
├── combo_stats.ipynb     # Data collection & cleaning notebook
├── matches.csv           # Collected match dataset
├── requirements.txt      # Python dependencies
└── README.md
```
