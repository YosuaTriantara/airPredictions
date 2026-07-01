import numpy as np

def predict_residual(model, xgb_input: np.ndarray) -> float:
    residual = model.predict(xgb_input)

    return float(residual[0])
