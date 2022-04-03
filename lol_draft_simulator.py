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
def read_data(): 
    """Read the picks and bans into lists."""
    # Create a global DataFrame that contains the pick/ban data
    global data
    data = pd.read_csv('picks_bans_2021.csv').fillna(method='ffill')

    # Create a global list that contains the selected champions
    global selected_champions
    selected_champions = []

def classify_picks_bans(phase):
    """Train a classifier to determine what champions are picked and banned.
    
    Args:
        phase (string): The given phase of the draft (ex: 'Blue Ban 1').
    """
    # Determine what phase is being classified
    target = data[phase]

    # Create Encoders and fit them to the data
    data_encoder = OrdinalEncoder().fit(data)
    target_encoder = LabelEncoder().fit(target)

    # Use the Encoders to transform the data
    encoded_data = data_encoder.transform(data)
    encoded_target = target_encoder.transform(target)

    # Split the data using an 80/20 split
    X_train, X_test, y_train, y_test = train_test_split(
        encoded_data, encoded_target, test_size = 0.2
    )

    # Create and train a Neural Network classifier
    classifier = MLPClassifier(max_iter = 1500)
    classifier.fit(X_train, y_train)
    
    # Predict the champion selected in the given phase (i.e., picked or banned)
    predictions = classifier.predict(X_test)

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

def simulate_draft():
    """Simulate the picks and bans."""
    # Classify the picks and bans of every phase
    # Ban phase one - each team takes turns banning champions
    classify_picks_bans('Blue Ban 1')
    classify_picks_bans('Red Ban 1')
    classify_picks_bans('Blue Ban 2')
    classify_picks_bans('Red Ban 2')
    classify_picks_bans('Blue Ban 3')
    classify_picks_bans('Red Ban 3')

    # Pick phase one - each team picks three champions, snake-style
    classify_picks_bans('Blue Pick 1')
    classify_picks_bans('Red Pick 1')
    classify_picks_bans('Red Pick 2')
    classify_picks_bans('Blue Pick 2')
    classify_picks_bans('Blue Pick 3')
    classify_picks_bans('Red Pick 3')

    # Ban phase two - each team takes turns banning champions
    classify_picks_bans('Red Ban 4')
    classify_picks_bans('Blue Ban 4')
    classify_picks_bans('Red Ban 5')
    classify_picks_bans('Blue Ban 5')

    # Pick phase two - each team picks two champions, snake-style
    classify_picks_bans('Red Pick 4')
    classify_picks_bans('Blue Pick 4')
    classify_picks_bans('Blue Pick 5')
    classify_picks_bans('Red Pick 5')

def print_draft():
    """Print the results of the draft in an easy-to-read format."""
    # Inform the user that the simulation
    print('\nDraft simulation finished! Results:\n')

    # List everything out
    print('Ban phase one - each team takes turns banning champions')
    print('\tBlue Ban 1:\t', selected_champions[0])
    print('\tRed Ban 1:\t', selected_champions[1])
    print('\tBlue Ban 2:\t', selected_champions[2])
    print('\tRed Ban 2:\t', selected_champions[3])
    print('\tBlue Ban 3:\t', selected_champions[4])
    print('\tRed Ban 3:\t', selected_champions[5])
    
    print('\nPick phase one - each team picks three champions, snake-style')
    print('\tBlue Pick 1:\t', selected_champions[6])
    print('\tRed Pick 1:\t', selected_champions[7])
    print('\tRed Pick 2:\t', selected_champions[8])
    print('\tBlue Pick 2:\t', selected_champions[9])
    print('\tBlue Pick 3:\t', selected_champions[10])
    print('\tRed Pick 3:\t', selected_champions[11])
    
    print('\nBan phase two - each team takes turns banning champions')
    print('\tRed Ban 4:\t', selected_champions[12])
    print('\tBlue Ban 4:\t', selected_champions[13])
    print('\tRed Ban 5:\t', selected_champions[14])
    print('\tBlue Ban 5:\t', selected_champions[15])
    
    print('\nPick phase two - each team picks two champions, snake-style')
    print('\tRed Pick 4:\t', selected_champions[16])
    print('\tBlue Pick 4:\t', selected_champions[17])
    print('\tBlue Pick 5:\t', selected_champions[18])
    print('\tRed Pick 5:\t', selected_champions[19])

if __name__ == '__main__':
    """Use the classifier to simulate the draft."""
    # Read in the data
    read_data()

    # Inform the user that the draft has started
    print('Simulating draft. Please wait, this could take a few minutes.')

    # Simulate the draft
    simulate_draft()

    # Inform the user that the draft is done and print the results
    # in an easy-to-read format
    print_draft()
