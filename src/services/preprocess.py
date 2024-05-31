import pandas as pd


def preprocess_data(input_df: pd.DataFrame):
    input_df = input_df.drop(columns=["mrg_", "pack", 'использование', 'регион', 'pack_freq'])
    input_df = input_df.assign(
        revenue_secret_score=input_df["доход"] * input_df["секретный_скор"],
        topup_freq_rev=input_df["частота_пополнения"] / input_df["доход"],
    )
    input_df = input_df.drop(columns="сегмент_arpu")
    client_id = input_df.pop("client_id")
    return input_df, client_id
