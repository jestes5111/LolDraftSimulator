#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""lol_draft_simulator.py: Use Neural Networks to simulate a
   League of Legends draft.
"""

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
def classify_picks_bans(data: np.array, phase: str) -> None:
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

    # Split 80% of the features into training features and 20% into testing features
    features_train, features_test, labels_train, labels_test = train_test_split(
        encoded_features, encoded_target, test_size = 0.2
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
        if selection in selected_champions:
            # Select another champion
            predictions.remove(selection)
        else:
            # Select the given champion and exit the loop
            selected_champions.append(str(selection[0]))
            break

def simulate_draft(data: np.array) -> None:
    """Simulate the picks and bans.

    Args:
        data: Champion selections and their selection phases
    """
    # Classify the picks and bans of every phase
    # Ban phase one - each team takes turns banning champions
    classify_picks_bans(data, 'Blue Ban 1')
    classify_picks_bans(data, 'Red Ban 1')
    classify_picks_bans(data, 'Blue Ban 2')
    classify_picks_bans(data, 'Red Ban 2')
    classify_picks_bans(data, 'Blue Ban 3')
    classify_picks_bans(data, 'Red Ban 3')

    # Pick phase one - each team picks three champions, snake-style
    classify_picks_bans(data, 'Blue Pick 1')
    classify_picks_bans(data, 'Red Pick 1')
    classify_picks_bans(data, 'Red Pick 2')
    classify_picks_bans(data, 'Blue Pick 2')
    classify_picks_bans(data, 'Blue Pick 3')
    classify_picks_bans(data, 'Red Pick 3')

    # Ban phase two - each team takes turns banning champions
    classify_picks_bans(data, 'Red Ban 4')
    classify_picks_bans(data, 'Blue Ban 4')
    classify_picks_bans(data, 'Red Ban 5')
    classify_picks_bans(data, 'Blue Ban 5')

    # Pick phase two - each team picks two champions, snake-style
    classify_picks_bans(data, 'Red Pick 4')
    classify_picks_bans(data, 'Blue Pick 4')
    classify_picks_bans(data, 'Blue Pick 5')
    classify_picks_bans(data, 'Red Pick 5')

def print_draft(selections: list) -> None:
    """Print the results of the draft in an easy-to-read format.

    Args:
        selections: List of champion selections
    """
    # Show the results of the draft
    print('Ban phase one - each team takes turns banning champions')
    print('\tBlue Ban 1:\t', selections[0])
    print('\tRed Ban 1:\t', selections[1])
    print('\tBlue Ban 2:\t', selections[2])
    print('\tRed Ban 2:\t', selections[3])
    print('\tBlue Ban 3:\t', selections[4])
    print('\tRed Ban 3:\t', selections[5])

    print('\nPick phase one - each team picks three champions, snake-style')
    print('\tBlue Pick 1:\t', selections[6])
    print('\tRed Pick 1:\t', selections[7])
    print('\tRed Pick 2:\t', selections[8])
    print('\tBlue Pick 2:\t', selections[9])
    print('\tBlue Pick 3:\t', selections[10])
    print('\tRed Pick 3:\t', selections[11])

    print('\nBan phase two - each team takes turns banning champions')
    print('\tRed Ban 4:\t', selections[12])
    print('\tBlue Ban 4:\t', selections[13])
    print('\tRed Ban 5:\t', selections[14])
    print('\tBlue Ban 5:\t', selections[15])

    print('\nPick phase two - each team picks two champions, snake-style')
    print('\tRed Pick 4:\t', selections[16])
    print('\tBlue Pick 4:\t', selections[17])
    print('\tBlue Pick 5:\t', selections[18])
    print('\tRed Pick 5:\t', selections[19])

if __name__ == '__main__':
    # Read in the data
    picks_bans = pd.read_csv('picks_bans_2021.csv').fillna(method='ffill')

    # Create a list to add selected champions to
    selected_champions = []

    # Inform the user that the draft has started
    print('Simulating draft. Please wait, this could take a few minutes.')

    # Simulate the draft
    simulate_draft(picks_bans)

    # Inform the user that the simulation is finished
    print('\nDraft simulation finished! Results:\n')

    # Print the results of the draft
    print_draft(selected_champions)
