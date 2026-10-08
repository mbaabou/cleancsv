import re


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


def find_email_columns(df):
    return [
        column
        for column in df.columns
        if "email" in column.lower()
        or "e-mail" in column.lower()
    ]


def count_invalid_emails(df):
    email_columns = find_email_columns(df)

    total_invalid = 0

    for column in email_columns:
        values = df[column].dropna().astype(str)

        for value in values:
            if not EMAIL_PATTERN.match(value.strip()):
                total_invalid += 1

    return total_invalid
