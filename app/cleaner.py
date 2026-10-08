import pandas as pd


def clean_dataframe(df: pd.DataFrame):
    original_rows = len(df)

    # Remove completely empty rows
    df = df.dropna(how="all")

    empty_rows_removed = original_rows - len(df)

    # Remove unnecessary spaces
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].apply(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    # Remove duplicate rows
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates()

    # Remove completely empty columns
    empty_columns = [
        column
        for column in df.columns
        if df[column].isna().all()
    ]

    df = df.drop(columns=empty_columns)

    # Count missing values
    missing_values = int(
        df.isna().sum().sum()
    )

    return df, {
        "original_rows": original_rows,
        "final_rows": len(df),
        "empty_rows_removed": empty_rows_removed,
        "duplicates_removed": duplicate_count,
        "empty_columns_removed": len(empty_columns),
        "missing_values": missing_values,
    }
