import numpy as np
import pandas as pd

WINDOW_SIZE = 24


def build_window(df_scaled: pd.DataFrame, window_size: int = WINDOW_SIZE) -> np.ndarray:

    if len(df_scaled) < window_size:
        raise ValueError(
            f"Butuh minimal {window_size} baris jam berturut-turut untuk 1 window, "
            f"tapi cuma tersedia {len(df_scaled)} baris valid. "
            "Cek gap/missing data pada rentang waktu OpenAQ yang diminta."
        )
    window = df_scaled.iloc[-window_size:].to_numpy()
    return window.reshape(1, window_size, window.shape[1])