import numpy as np

def predict(model, scaler_y, lstm_input: np.ndarray) -> float:
    scaled_prediction = model.predict(
        lstm_input,
        verbose=0
    )

    actual_prediction = scaler_y.inverse_transform(scaled_prediction)
    return float(actual_prediction[0][0])
