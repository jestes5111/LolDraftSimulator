#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use Neural Networks to simulate a League of Legends draft."""

__file__ = 'lol_draft_simulator.py'
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

# Third-party libraries
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

# Owned libraries

# --------------------------------------------------------------------------- #
#                                    Code                                     #
# --------------------------------------------------------------------------- #
def classify_picks_bans(
    data: pd.DataFrame,
    phase: str,
    selections: list
) -> None:
  """Use a Neural Network to classify champions selected in the given phase.

  Args:
      data: Champion selections and their selection phases
      phase: Draft phase that the champion was selected in
  """
  # Determine what phase is being classified
  target = data[phase]

  # Create a modified copy of the DataFrame excluding the current phase
  features = data.drop(phase, axis=1)

  # Use Encoders to make the data readable by the Neural Network
  features_encoder = OrdinalEncoder().fit(features)
  encoded_features = features_encoder.transform(features)
  target_encoder = LabelEncoder().fit(target)
  encoded_target = target_encoder.transform(target)

  # Split 80% of the features into training and 20% into testing
  features_train, features_test, labels_train, labels_test = train_test_split(
    encoded_features, encoded_target, test_size=0.2
  )

  # Remove the unused 'labels_test' variable
  del labels_test

  # Create and train a Neural Network classifier
  classifier = MLPClassifier(max_iter=1500)
  classifier.fit(features_train, labels_train)

  # Determine the champion selected in the given phase (i.e., picked or banned)
  predictions = classifier.predict(features_test)

  # Un-encode the features (i.e., revert it to champion name)
  predictions = target_encoder.inverse_transform(predictions)

  # Remove duplicates
  predictions = list(set(predictions))

  # Check if the selected champion was previously selected
  for selection in predictions:
    # Select a random champion
    selection = np.random.choice(predictions, 1)

    # Check if the champion was selected
    if selection in selections:
      # Select another champion
      predictions.remove(selection)
    else:
      # Get the given champion's name, select them, and exit the loop
      selections.append(str(selection[0]))
      break

if __name__ == '__main__':
  # Read in the data
  picks_bans = pd.read_csv('picks_bans_2021.csv').fillna(method='ffill')

  # Create a list to add selected champions to
  selected_champions = []

  # Create a counter to show what selection is being looked at
  selection_counter = 0

  # Simulate the draft
  print('Beginning draft simulation.')
  for draft_phase in picks_bans.columns:
    classify_picks_bans(picks_bans, draft_phase, selected_champions)

    # Print a blank line for formatting
    if draft_phase in ['Blue Ban 1', 'Blue Pick 1', 'Red Ban 4', 'Red Pick 4']:
      print()
    
    # Print the selection and look at the next selection
    print('\t'+ draft_phase + ':\t', selected_champions[selection_counter])
    selection_counter += 1

  # End of program
  print('\nDraft simulation finished!')
