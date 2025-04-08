import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def load_data(filename='TOTALmatchdata.csv'):
    data = pd.read_csv(filename)

    # Features: all columns except 'label'
    X = data.drop('label', axis=1).values


    y = data['label'].values

    return X, y


def preprocess_data(X, y):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

 
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, scaler

def build_and_train_model(X_train, y_train, X_test, y_test):
    model = Sequential([
        Dense(64, activation='relu', input_dim=X_train.shape[1]),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=20, batch_size=4, validation_data=(X_test, y_test))

    return model


def save_model(model, filename='league_win_predictor.h5'):
    model.save(filename)


def main():
    X, y = load_data('TOTALmatchdata.csv')
    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)
    model = build_and_train_model(X_train, y_train, X_test, y_test)

    loss, acc = model.evaluate(X_test, y_test)
    print(f"Model accuracy: {acc * 100:.2f}%")

    model.save("league_win_predictor.keras")
    print("Model saved as 'league_win_predictor.keras'")

if __name__ == "__main__":
    main()
