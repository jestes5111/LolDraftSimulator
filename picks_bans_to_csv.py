#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Scrape Leaguepedia for picks and bans and create a CSV file with the data."""

__file__ = 'picks_bans_to_csv.py'
__author__ = 'Jesse Estes'
__copyright__ = 'Copyright 2022, LolDraftSimulator'
__credits__ = ['Jesse Estes']
__license__ = 'MIT'
__version__ = '1.0.1'
__maintainer__ = 'Jesse Estes'
__email__ = 'jestes5111@gmail.com'
__status__ = 'Prototype'

# --------------------------------------------------------------------------- #
#                                  Imports                                    #
# --------------------------------------------------------------------------- #
# Standard libraries
import sys

# Third-party libraries
import leaguepedia_parser
import lol_id_tools as lit
import pandas as pd

# Owned libraries

# --------------------------------------------------------------------------- #
#                                    Code                                     #
# --------------------------------------------------------------------------- #
# Initialize a dictionary to store data
draft_dict = {
  'Blue Ban 1': [],
  'Red Ban 1': [],
  'Blue Ban 2': [],
  'Red Ban 2': [],
  'Blue Ban 3': [],
  'Red Ban 3': [],
  'Blue Pick 1': [],
  'Red Pick 1': [],
  'Red Pick 2': [],
  'Blue Pick 2': [],
  'Blue Pick 3': [],
  'Red Pick 3': [],
  'Red Ban 4': [],
  'Blue Ban 4': [],
  'Red Ban 5': [],
  'Blue Ban 5': [],
  'Red Pick 4': [],
  'Blue Pick 4': [],
  'Blue Pick 5': [],
  'Red Pick 5': [],
}

# Read command line arguments to get the desired year
desired_year = sys.argv[1]

# Create a list of names of regions
region_names = ['China', 'Europe', 'Korea', 'North America']

# Create a list of the names of tournaments
tournament_names = [
  'LPL/' + str(desired_year) + ' Season/Spring Season',
  'LPL/' + str(desired_year) + ' Season/Summer Season',
  'LEC/' + str(desired_year) + ' Season/Spring Season',
  'LEC/' + str(desired_year) + ' Season/Summer Season',
  'LCK/' + str(desired_year) + ' Season/Spring Season',
  'LCK/' + str(desired_year) + ' Season/Summer Season',
  'LCS/' + str(desired_year) + ' Season/Spring Season',
  'LCS/' + str(desired_year) + ' Season/Summer Season',
]

# Get the reigons
regions = leaguepedia_parser.get_regions()

# Loop through the list of region names
for region_name in region_names:
  # Get tournaments from the 2021 season of the specified region
  tournaments = leaguepedia_parser.get_tournaments(region_name, year=int(desired_year))

# Loop through the list of tournament names
for tournament_name in tournament_names:
  # Get all games from the specified tournament
  games = leaguepedia_parser.get_games(tournament_name)

  # Loop through all the games from the specified list
  for game in games:
    # Get the details of the current game
    current_game = leaguepedia_parser.get_game_details(game)

    # Save the picks and bans of the current game
    picks_bans = current_game.picksBans

    # Save the teams playing in the current gamee
    teams = current_game.teams

    # Set up pick/ban counters for each team
    count_blue_ban = 0
    count_red_ban = 0
    count_blue_pick = 0
    count_red_pick = 0

    # Loop through all picks and bans
    for champion in picks_bans:
      # Check if the champion was picked or banned
      if champion.isBan:
        # Check what team banned the champion
        if champion.team == 'BLUE' and count_blue_ban < 5:
          # Increment the counter
          count_blue_ban += 1

          # Create a string to use as the dictionary index
          result = 'Blue Ban ' + str(count_blue_ban)
        elif count_red_ban < 5:
          # Increment the counter
          count_red_ban += 1

          # Create a string to use as the dictionary index
          result = 'Red Ban ' + str(count_red_ban)

        # Store the draft data in the dictionary
        draft_dict[result].append(
          lit.get_name(champion.championId, object_type='champion')
        )
      else:
        # Check what team picked the champion
        if champion.team == 'BLUE' and count_blue_pick < 5:
          # Increment the counter
          count_blue_pick += 1

          # Create a string to use as the dictionary index
          result = 'Blue Pick ' + str(count_blue_pick)
        elif count_red_pick < 5:
          # Increment the counter
          count_red_pick += 1

          # Create a string to use as the dictionary index
          result = 'Red Pick ' + str(count_red_pick)

        # Store the draft data in the dictionary
        draft_dict[result].append(
          lit.get_name(champion.championId, object_type='champion')
        )

# Create a DataFrame using the dictionary
data = pd.DataFrame(draft_dict)

# Shuffle the DataFrame
data = data.sample(frac=1)

# Send the DataFrame to a csv file for reading
data.to_csv('picks_bans_' + str(desired_year) + '.csv', index=False)
