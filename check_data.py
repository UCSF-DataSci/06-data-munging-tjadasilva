import pandas as pd

# Load the messy dataset
df = pd.read_csv('messy_population_data.csv')

# Display initial information
print("Data Information:")
print(df.info())

print("\nData Description:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Identify categorical columns (object data type)
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

# Display group counts and proportions for identified categorical columns
for column in categorical_columns:
    print(f"\n{column} - Value Counts:")
    print(df[column].value_counts(dropna=False))  # Include NaN values in the counts
    print(f"\n{column} - Proportions:")
    print(df[column].value_counts(normalize=True, dropna=False))  # Include NaN values in proportions
