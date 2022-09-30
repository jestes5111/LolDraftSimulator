#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Use Neural Networks to simulate a League of Legends draft."""

__file__ = 'lol_draft_simulator.py'
__author__ = 'Jesse Estes'
__copyright__ = 'Copyright 2022, LolDraftSimulator'
__credits__ = ['Jesse Estes']
__license__ = 'MIT'
__version__ = '1.0.2'
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
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Owned libraries

# --------------------------------------------------------------------------- #
#                                    Code                                     #
# --------------------------------------------------------------------------- #
def main() -> None:
  """Read the data to be used and simulate the draft."""
  # Read in the data and fill missing values
  filename = 'data/picks_bans_LCK-LCS-LEC-LPL_2021.csv'
  selection_data = pd.read_csv(filename).fillna(method='ffill')

  # Create a list to add selected champions to
  selected_champions = []

  # Create a counter to show what selection is being looked at
  selection_counter = 0

  # Simulate the draft
  print('Beginning draft simulation.')
  for draft_phase in selection_data.columns:
    select_champions(selection_data, draft_phase, selected_champions)

    # Print a blank line in certain spots for formatting
    if draft_phase in ['Blue Ban 1', 'Blue Pick 1', 'Red Ban 4', 'Red Pick 4']:
      print()

    # Print the selection and look at the next selection
    print('\t'+ draft_phase + ':\t', selected_champions[selection_counter])
    selection_counter += 1

  # End of program
  print('\nDraft simulation finished!\n')

def select_champions(
    data: pd.DataFrame,
    phase: str,
    selections: list
) -> None:
  """Use Neural Networks to classify champions selected in the given phase.

  Args:
      data: Champion selections and their selection phases
      phase: Draft phase that the champion was selected in
      selections: List of champions that have been selected
  """
  # Determine what phase is being classified
  target = data[phase]

  # Create a modified copy of the DataFrame that excludes the current phase
  features = data.loc[:, :phase]
  features = features.drop(phase, axis=1)

  # Use Encoders to make the data readable by the Neural Network
  features_encoder = OrdinalEncoder().fit(features)
  features = features_encoder.transform(features)
  target_encoder = LabelEncoder().fit(target)
  target = target_encoder.transform(target)

  # Split features to be 80% training and 20% testing
  X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2
  )

  # Create and train a StandardScaler
  scaler = StandardScaler()
  scaler.fit(X_train)

  # Scale the data
  X_train = scaler.transform(X_train)
  X_test = scaler.transform(X_test)

  # Remove unused variable
  del y_test

  # Create and train a Neural Network classifier
  classifier = MLPClassifier(max_iter=2500)
  classifier.fit(X_train, y_train)

  # Determine the champion selected (picked or banned) in the given phase
  predictions = classifier.predict(X_test)

  # Un-encode the potential selections (i.e., revert to champion name)
  predictions = target_encoder.inverse_transform(predictions)

  # Remove duplicates and previously selected champions
  predictions = list(set(predictions) - set(selections))

  # Choose a random champion and add them to the list of selected champions
  selection = np.random.choice(predictions, 1)
  selections.append(str(selection[0]))

if __name__ == '__main__':
  main()