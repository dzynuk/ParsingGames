# ParsingGames
Steam Game Data Collection

This repository contains code for collecting data about RTS games from Steam (https://store.steampowered.com/search/?tags=1676&category1=998&supportedlang=english&ndl=1).

Files

The repository includes the following files:

    collectallgames.py: Python script for data collection from Steam.
    Sortedtop150games.py: Python script for sorting games.
    Output/: Folder containing the following generated files:
        allgames.csv: CSV file containing data about the collected games.
        top150games.csv: CSV file containing data about the top 150 games.

Data Collection Process

Data collection: The collectallgames.py script collects data from Steam by gathering all RTS games with good evaluations and then retrieving all the necessary information about the selected games.

Data processing: The collected data is processed using Sortedtop150games.py script, where games with a 'Review' count greater than or equal to 1000 are sorted based on the 'Rating', 'Positive Review', and 'Review' values.

Contact

If you have any questions or suggestions, please feel free to contact us at dzhunmykola@gmail.com.
