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

# Read command line arguments to get the desired region(s) and year(s) as lists
regions = sys.argv[1].split(',')
years = sys.argv[2].split(',')

# Convert values to int
years = list(map(int, years))

# Create a list of tournament names and populate based on selections
tournament_names = []
for year in years:
  if 'China' in regions:
    tournament_names.append('LPL/' + str(year) + ' Season/Spring Season')
    tournament_names.append('LPL/' + str(year) + ' Season/Summer Season')

  if 'Korea' in regions:
    tournament_names.append('LCK/' + str(year) + ' Season/Spring Season')
    tournament_names.append('LCK/' + str(year) + ' Season/Summer Season')

  if ('Europe' in regions) and (year >= 2019):
    tournament_names.append('LEC/' + str(year) + ' Season/Spring Season')
    tournament_names.append('LEC/' + str(year) + ' Season/Summer Season')
  elif ('Europe' in regions) and (2019 > year >= 2013):
    tournament_names.append('EU_LCS/' + str(year) + ' Season/Spring Season')
    tournament_names.append('EU_LCS/' + str(year) + ' Season/Summer Season')

  if ('North America' in regions) and (year >= 2019):
    tournament_names.append('LCS/' + str(year) + ' Season/Spring Season')
    tournament_names.append('LCS/' + str(year) + ' Season/Summer Season')
  elif ('North America' in regions) and (2019 > year >= 2013):
    tournament_names.append('NA_LCS/' + str(year) + ' Season/Spring Season')
    tournament_names.append('NA_LCS/' + str(year) + ' Season/Summer Season')

# Get the regions from Leaguepedia
regions_leaguepedia = leaguepedia_parser.get_regions()

# Loop through the list of years
for year in years:
  # Loop through the list of region names
  for region in regions:
    # Get tournaments from the 2021 season of the specified region
    tournaments = leaguepedia_parser.get_tournaments(region, year=year)

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

# Create a string of the given regions to use in the filename
regions_list = []
if 'China' in regions:
  regions_list.append('CN')
if 'Europe' in regions:
  regions_list.append('EU')
if 'Korea' in regions:
  regions_list.append('KR')
if 'North America' in regions:
  regions_list.append('NA')
filename_regions = '-'.join(regions_list) + '_'

# Create a string of the given years to use in the filename
years_list = list(map(str, years))
filename_years = '_'.join(years_list)

# Create the filename by putting the substrings together
filename = 'picks_bans_' + filename_regions + filename_years + '.csv'

# Send the DataFrame to a csv file for reading
data.to_csv(filename, index=False)
