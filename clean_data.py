import pandas as pd

# Load the dataset
df = pd.read_csv('messy_population_data.csv')

# Initial row count
initial_row_count = len(df)

# Step 1: Remove Duplicate Rows
df_cleaned = df.drop_duplicates().copy()
duplicate_count = initial_row_count - len(df_cleaned)
print(f"Removed {duplicate_count} duplicate rows.")

# Step 2: Convert Gender Column to Categorical and Start Handling Missing Data
# Fill missing gender with 99
missing_gender_before = df_cleaned['gender'].isnull().sum()
df_cleaned.loc[:, 'gender'].fillna(99, inplace=True)
df_cleaned['gender'] = df_cleaned['gender'].astype('category').cat.rename_categories({
    1: '1 (Male?)',
    2: '2 (Female?)',
    3: '3 (Other?)',
    99: 'Unknown'
})

# Rename categories:
df_cleaned['gender'] = df_cleaned['gender'].cat.rename_categories({1: '1 (Male?)', 2: '2 (Female?)', 3: '3 (Other?)', 99: 'Unknown'})
print("Converted 'gender' to categorical.")

# Step 3: Handle Missing Values 
# Track missing values before filling
missing_income_before = df_cleaned['income_groups'].isnull().sum()
missing_age_before = df_cleaned['age'].isnull().sum()
missing_year_before = df_cleaned['year'].isnull().sum()
missing_population_before = df_cleaned['population'].isnull().sum()

# Fill missing values for categorical and numerical columns
df_cleaned.loc[:, 'income_groups'].fillna('Unknown', inplace=True)
df_cleaned.loc[:, 'age'].fillna(df_cleaned['age'].mean(), inplace=True)
df_cleaned.loc[:, 'year'].fillna(df_cleaned['year'].median(), inplace=True)
df_cleaned.loc[:, 'population'].fillna(df_cleaned['population'].median(), inplace=True)

# Track how many rows were affected by missing value filling
missing_income_after = df_cleaned['income_groups'].isnull().sum()
missing_age_after = df_cleaned['age'].isnull().sum()
missing_gender_after = df_cleaned['gender'].isnull().sum()
missing_year_after = df_cleaned['year'].isnull().sum()
missing_population_after = df_cleaned['population'].isnull().sum()

print(f"Filled {missing_income_before - missing_income_after} missing 'income_groups' values.")
print(f"Filled {missing_age_before - missing_age_after} missing 'age' values.")
print(f"Filled {missing_gender_before - missing_gender_after} missing 'gender' values.")
print(f"Filled {missing_year_before - missing_year_after} missing 'year' values.")
print(f"Filled {missing_population_before - missing_population_after} missing 'population' values.")

# Step 4: Clean Typos and Convert 'income_groups' Column to Numeric Categories
# Create a mapping to fix the typos and convert the income groups to numeric categories
income_group_mapping = {
    'lower_middle_income_typo': 'lower_middle_income',
    'low_income_typo': 'low_income',
    'high_income_typo': 'high_income',
    'upper_middle_income_typo': 'upper_middle_income',
    'low_income': 1,
    'lower_middle_income': 2,
    'upper_middle_income': 3,
    'high_income': 4,
    'Unknown': 99
}

# Track rows before and after replacing typos
typos_before = df_cleaned['income_groups'].isin(income_group_mapping.keys()).sum()

# Replace the typos with the correct categories
df_cleaned.loc[:, 'income_groups'].replace(income_group_mapping, inplace=True)

# Convert the income group column to numeric categories based on the mapping
df_cleaned['income_groups'] = df_cleaned['income_groups'].astype('category').replace({
    'low_income': 1,
    'lower_middle_income': 2,
    'upper_middle_income': 3,
    'high_income': 4,
    'Unknown': 99
})

# Rename the numeric categories with appropriate labels
df_cleaned['income_groups'] = df_cleaned['income_groups'].cat.rename_categories({
    1: 'Low Income',
    2: 'Lower Middle Income',
    3: 'Upper Middle Income',
    4: 'High Income',
    99: 'Unknown'
})

# Track rows after converting to numeric categories
typos_after = df_cleaned['income_groups'].isin(income_group_mapping.keys()).sum()
print(f"Corrected {typos_before - typos_after} rows with income group typos and converted to numeric categories.")

# Step 5: Correct Year Typos
# Track year correction counts
invalid_years_2025_2099_before = df_cleaned[(df_cleaned['year'] >= 2025) & (df_cleaned['year'] <= 2099)].shape[0]
invalid_years_2100_plus_before = df_cleaned[df_cleaned['year'] >= 2100].shape[0]

# Correct years if they are between 2025-2099 (as 19XX) or >=2100 (as 20XX)
df_cleaned.loc[:, 'year'] = df_cleaned['year'].apply(lambda x: x - 100 if 2025 <= x <= 2099 or x >= 2100 else x)

# Track year correction results
invalid_years_2025_2099_after = df_cleaned[(df_cleaned['year'] >= 2025) & (df_cleaned['year'] <= 2099)].shape[0]
invalid_years_2100_plus_after = df_cleaned[df_cleaned['year'] >= 2100].shape[0]

print(f"Changed {invalid_years_2025_2099_before - invalid_years_2025_2099_after} rows with years between 2025-2099.")
print(f"Changed {invalid_years_2100_plus_before - invalid_years_2100_plus_after} rows with years >=2100.")

# Step 6: Compare Data Distribution Before and After Cleaning
# Load the original dataset for comparison
df_original = pd.read_csv('messy_population_data.csv')

# Display summary statistics for the original and cleaned datasets, excluding 'income_groups'
print("\n--- Data Distribution: Original Dataset ---")
print(df_original.describe(include=[float]))

print("\n--- Data Distribution: Cleaned Dataset ---")
print(df_cleaned.describe(include=[float]))

# Identify categorical columns
categorical_columns_original = df_original.select_dtypes(include=['object', 'category']).columns.tolist()
categorical_columns_cleaned = df_cleaned.select_dtypes(include=['object', 'category']).columns.tolist()

with open('data_distribution_comparison.txt', 'w') as file:
    # Write numerical descriptions (excluding income_groups)
    file.write("--- Data Distribution: Original Dataset (Numerical) ---\n")
    file.write(str(df_original.drop(columns=['income_groups'], errors='ignore').describe(include=[float])))
    
    file.write("\n\n--- Data Distribution: Categorical Counts (Original) ---\n")
    # Write value counts for each categorical column in the original dataset
    for col in categorical_columns_original:
        file.write(f"\nProportions for {col} (Original):\n")
        file.write(str(df_original[col].value_counts(normalize=True) * 100))
    
    # Write numerical descriptions for cleaned dataset (excluding income_groups)
    file.write("\n\n--- Data Distribution: Cleaned Dataset (Numerical) ---\n")
    file.write(str(df_cleaned.drop(columns=['income_groups'], errors='ignore').describe(include=[float])))
    
    file.write("\n\n--- Data Distribution: Categorical Counts (Cleaned) ---\n")
    # Write value counts for each categorical column in the cleaned dataset
    for col in categorical_columns_cleaned:
        file.write(f"\nProportions for {col} (Cleaned):\n")
        file.write(str(df_cleaned[col].value_counts(normalize=True) * 100))

print("Data distribution comparison saved to 'data_distribution_comparison.txt'.")

# Step 7: Save the Cleaned Dataset
df_cleaned.to_csv('cleaned_population_data.csv', index=False)
print("Cleaned dataset saved to 'cleaned_population_data.csv'.")
