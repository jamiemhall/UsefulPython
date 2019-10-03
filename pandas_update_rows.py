import pandas as pd


def update_row_values(row: pd.Series) -> pd.Series:
    return pd.Series({
        'City': row['City'].title(),
        'Weight': row['Weight'] - 5,
        'Height': row['Height'],
        'Age': row['Age'] + 3,
    })


def main():
    data = {'City': ['rome', 'madrid', 'new York', 'oxford', 'Berlin'],
            'Weight': [60, 83, 50, 100, 70],
            'Height': [160, 155, 178, 165, 135],
            'Age': [25, 94, 57, 62, 70]}
    df = pd.DataFrame(data, index=['Jason', 'Molly', 'Tina', 'Jake', 'Amy'])

    print(df)
    df_updated = df.apply(update_row_values, axis='columns')
    print(df_updated)


if __name__ == "__main__":
    main()
