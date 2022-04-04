#!/usr/bin/env python
"""lol_draft_simulator.py: Use Neural Networks to simulate a
   League of Legends draft.
"""

# --------------------------------------------------------------------------- #
#                                  Imports                                    #
# --------------------------------------------------------------------------- #
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

# --------------------------------------------------------------------------- #
#                                    Code                                     #
# --------------------------------------------------------------------------- #
def classify_picks_bans(data, phase):
    """Train a classifier to determine what champions are picked and banned.
    
    Args:
        phase (string): The given phase of the draft (ex: 'Blue Ban 1').
    """
    # Determine what phase is being classified
    target = data[phase]

    # Create Encoders and fit them to the data
    data_encoder = OrdinalEncoder().fit(data)
    target_encoder = LabelEncoder().fit(target)

    # Transform the data to make it readable by the Neural Network 
    encoded_data = data_encoder.transform(data)
    encoded_target = target_encoder.transform(target)

    # Split the data using an 80/20 split
    features_train, features_test, labels_train, labels_test = train_test_split(
        encoded_data, encoded_target, test_size = 0.2
    )

    # Remove the unused 'labels_test' variable
    del labels_test

    # Create and train a Neural Network classifier
    classifier = MLPClassifier(max_iter = 1500)
    classifier.fit(features_train, labels_train)
    
    # Predict the champion selected in the given phase (i.e., picked or banned)
    predictions = classifier.predict(features_test)

    # Revert to the original form of data (champion name)
    predictions = target_encoder.inverse_transform(predictions)

    # Remove duplicates from the list of predictions
    predictions = list(set(predictions))

    # Check if the selected champion has already been selected
    for selection in predictions:
        # Grab a random champion from the predictions
        selection = np.random.choice(predictions, 1)

        # Check if the champion was selected
        if selection in selected_champions:
            # If the champion has been selected, remove it from the list
            # and select another champion
            predictions.remove(selection)
        else:
            # If the champion has not been selected, select it
            selected_champions.append(str(selection[0]))

            # Exit the loop since the selection has been made
            break

def simulate_draft(data):
    """Simulate the picks and bans."""
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

def print_draft(selections):
    """Print the results of the draft in an easy-to-read format."""
    # Inform the user that the simulation
    print('\nDraft simulation finished! Results:\n')

    # List everything out
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

    # Inform the user that the draft is done and print the results
    # in an easy-to-read format
    print_draft(selected_champions)
