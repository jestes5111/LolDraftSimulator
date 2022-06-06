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
import os
import sys

# Third-party libraries
import leaguepedia_parser
import lol_id_tools as lit
import pandas as pd

# Owned libraries

# --------------------------------------------------------------------------- #
#                                    Code                                     #
# --------------------------------------------------------------------------- #
# Tell the user that the script is running
print('Pick/ban data collection script starting.')

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

# Read command line arguments to get the desired region(s) and year(s) as lists
regions = sys.argv[1].split(',')
years = sys.argv[2].split(',')

# Convert year values to int
years = list(map(int, years))

# Remove duplicates from and sort the list of years (safety check)
years = list(set(years))
years.sort()

# Create lists of tournament names and region names
tournament_names = []
region_names = []

# Populate the lists based on user input
for year in years:
  for region in regions:
    # Get the tournaments from the given region and year
    tournaments = leaguepedia_parser.get_tournaments(region, year=year)

    # Dynamically add the spring and summer seasons to the lists
    for tournament in range(len(tournaments)):
      if ('Spring Season' in tournaments[tournament].overviewPage or
          'Summer Season' in tournaments[tournament].overviewPage):
        tournament_names.append(tournaments[tournament].overviewPage)
        region_names.append(tournaments[tournament].leagueShort)

# Remove duplicates from the list of region names
region_names = list(set(region_names))

# Put the list in alphabetical order
region_names.sort()

# Loop through the list of tournament names
for tournament_name in tournament_names:
  # Tell the user what tournament data is being collected for
  print('\nCollecting data from ' + tournament_name + ', please wait.')

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

  # Tell the user that data collection for the current tournament is completed
  print('Data from ' + tournament_name + ' collected!')

# Create a DataFrame using the dictionary
data = pd.DataFrame(draft_dict)

# Shuffle the DataFrame
data = data.sample(frac=1)

# Create a folder to store the created files if it doesn't exist already
if not os.path.isdir('data'):
  os.mkdir('data')

# Remove 'NA LCS' from the list, use 'LCS' readability
if 'NA LCS' in region_names:
  region_names.remove('NA LCS')

  # Append 'LCS' in case it is not already in the list
  region_names.append('LCS')

# Same for 'EU LCS' and 'LEC'
if 'EU LCS' in region_names:
  region_names.remove('EU LCS')

  # Append 'LEC' in case it is not already in the list
  region_names.append('LEC')

# Remove potential new duplicates from and sort the list of region names,
# does nothing if nothing was added
region_names = list(set(region_names))
region_names.sort()

# Create a string of the given regions to use in the filename
filename_regions = '-'.join(region_names) + '_'

# Create a string of the given years to use in the filename
years_list = list(map(str, years))
filename_years = '-'.join(years_list)

# Create the filename by putting the substrings together
filename = 'data/picks_bans_' + filename_regions + filename_years + '.csv'

# Send the DataFrame to a csv file for reading
data.to_csv(filename, index=False)

# Inform the user that the script has finished
print('\nPick/ban data collection script finished!')
