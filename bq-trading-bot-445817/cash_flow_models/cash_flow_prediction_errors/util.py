import pandas as pd


def merge(left: pd.DataFrame, right: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    return left.merge(right, on=keys)
