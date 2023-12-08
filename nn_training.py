"""
This module is used for training the NN model to classify team compositions
against their win percent
"""


import tensorflow as tf
import pandas as pd
import json
import os
from sklearn.model_selection import train_test_split


CHAMP_LIST = ['Archer', 'Fighter', 'Knight', 'Monk', 'Ninja', 'Priestess',
            'Pyromancer', 'Swordsman', 'Shrine Maiden', 'Berserker', 'Sniper',
            'Ice Mage', 'Magic Knight', 'Shield Bearer', 'Ghost',
            'Lightning Mage', 'Necromancer', 'Boomerang Hunter',
            'Plague Doctor', 'Poison Dart Hunter', 'Barrier Mage', 'Vampire',
            'Devil', 'Gambler', 'Lancer', 'Dual Blader', 'Executioner',
            'Bard', 'Gunner', 'Illusionist', 'Shadowmancer', 'Cook',
            'Exorcist', 'Clown', 'Ogre', 'Werewolf', 'Taoist',
            'Mystic Dancer', 'Dark Mage', 'Cold Corpse']


def encode_characters(data):
    # Create dataframe
    df = pd.DataFrame(data)

    # Initialize with 0 for all characters
    for char in CHAMP_LIST:
        df[char] = 0

    # Set encoding values based on characters in the data set
    for index, row in df.iterrows():
        team1 = row['characters'][:4]
        team2 = row['characters'][4:]

        for char in team1:
            df.at[index, char] = 1
        for char in team2:
            df.at[index, char] = -1

    # Drop original 'characters' column
    df = df.drop('characters', axis = 1)

    return df


# Encode result as 1 for 'win' and 0 for 'loss'
def encode_result(data):
    for entry in data:
        if entry['result'] == 'Win':
            entry['result'] = 1
        elif entry['result'] == 'Loss':
            entry['result'] = 0


def main():
    # Define JSON file path
    #current_dir = os.path.join(os.path.dirname(__file__))
    # 'data' is folder and 'data.json' is file name
    #json_file = os.path.join(os.path.dirname(__file__), 'data', 'data.json')
    json_file = 'data.json'

    # Load data from JSON file
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    # Encode the data
    encode_result(json_data)
    encoded_data = encode_characters(json_data)

    # Split data into training, validation, and testing sets
    # 80% training, 20% testing
    y_train = encoded_data['result']
    x_train = encoded_data.drop('result', axis = 1)
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
                                                        test_size = 0.2,
                                                        random_state = 420)
    # Split test data into 50% validation and 50% test
    x_val, x_test, y_val, y_test = train_test_split(x_test, y_test,
                                                    test_size = 0.5,
                                                    random_state = 420)
    '''
    print(train_data)
    print(validation_data)
    print(test_data)
    '''

    # Reshape the data
    x_train_np = x_train.to_numpy()
    x_train = x_train_np.reshape(x_train_np.shape[0], 40, 1)
    x_val_np = x_val.to_numpy()
    x_val = x_val_np.reshape(x_val_np.shape[0], 40, 1)
    x_test_np = x_test.to_numpy()
    x_test = x_test_np.reshape(x_test_np.shape[0], 40, 1)

    model = tf.keras.Sequential([
        # Input shape corresponds to hot-encoded one
        tf.keras.layers.Input(shape=(40, 1)),
        tf.keras.layers.LSTM(32, return_sequences = True),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation = 'relu'),
        tf.keras.layers.Dense(64, activation = 'relu'),
        tf.keras.layers.Dense(2, activation = 'softmax')
    ])

    # Compile and train
    model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy',
                    metrics=['accuracy'])
    model.fit(x_train, y_train,
                validation_data = (x_val, y_val),
                epochs = 10, batch_size = 32)

    # Test the accuracy of the model
    test_loss, test_accuracy = model.evaluate(x_test, y_test)
    print(f'Test Accuracy: {test_accuracy}')

    # Save the Model
    model.save('my_model.h5')

if __name__ == '__main__':
    main()