# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125,718 entries
- **Columns**: 5 columns

### Column Details
| Column         | Data Type | Non-Null Count | Missing Values | Description                                     |
|----------------|-----------|----------------|----------------|-------------------------------------------------|
| income_groups  | object    | 119,412        | 6,306          | Categorical column indicating income group.      |
| age            | float64   | 119,495        | 6,223          | Numeric column representing age.                 |
| gender         | float64   | 119,811        | 5,907          | Numeric column representing gender.              |
| year           | float64   | 119,516        | 6,202          | Numeric column representing the year.            |
| population     | float64   | 119,378        | 6,340          | Numeric column representing the population size. |

### Identified Issues

1. **Missing Values**
   - **Description:** 
   All columns have missing values:
    - Income_groups has 6,306 missing entries.
    - Age has 6,223 missing entries.
    - Gender has 5,907 missing entries.
    - Year has 6,202 missing entries.
    - Population has 6,340 missing entries.
   - **Impact:** Missing values may introduce bias in the analysis or reduce the available sample size.

2. **Data Types:**
   - **Description**: The gender column is currently stored as a numerical type, but it represents categorical data with three distinct values: 1, 2, and 3. The income_groups column is nominal but represents an ordered categorical variable (e.g., low_income < lower_middle_income < upper_middle_income < high_income), and should be changed to a categorical variable for more accurate analysis.

3. **Duplicates:**
   - **Description:** There are 2,950 duplicate rows found in the dataset.
   - **Impact:** Duplicate rows can distort analysis, leading to over-representation of certain population segments.

4. **Additional errors:**
   - **Income:** The income groups column contains several values typos, such as lower_middle_income_typo, low_income_typo, high_income_typo, and upper_middle_income_typo. These incorrect values need to be cleaned and replaced with their correct counterparts (lower_middle_income, low_income, high_income, and upper_middle_income).
   - **Gender:** Typically, gender is represented as 1 (or 0) for male and 2 (or 1) for female. Therefore, without further clarification, the presence of gender=3 could lead to inaccurate gender-based analysis unless the value is properly understood and handled, ideally with the help of a dataset codebook.
   - **Year:** The year column spans from 1950 to 2119, which includes both past and future years.Depending on the focus of the analysis, the inclusion of future years might indicate an error.

# 2. Data Cleaning Process

### Issue 1: Duplicate Rows
- **Cleaning Method:** Removed duplicate rows using df.drop_duplicates().
- **Implementation:**
  ```python
  df_cleaned = df.drop_duplicates()
  ```
- **Justification:** drop_duplicates() is a simple and efficient method provided by Pandas that removes entire duplicate rows, preserving only the first occurrence.
- **Impact:** 
  - Rows affected: 2,950 duplicate rows removed.
  - Data distribution change: Minimal effect on data distribution, but ensures unique representation of each observation.

### Issue 2: Missing Values
- **Cleaning Method:** Filled missing values in income_groups and gender with 99 or 'Unknown'. Filled missing values in age, year, and population columns with the mean or median values.
- **Implementation:**
  ```python
  df_cleaned['income_groups'].fillna('Unknown', inplace=True)
  df_cleaned['age'].fillna(df_cleaned['age'].mean(), inplace=True)
  df_cleaned['gender'].fillna(99, inplace=True)
  df_cleaned['year'].fillna(df_cleaned['year'].median(), inplace=True)
  df_cleaned['population'].fillna(df_cleaned['population'].median(), inplace=True)
  ```
- **Justification:** Categorical missing values are best filled with a placeholder ('Unknown'), while numeric missing values can be imputed using statistical measures like mean/median to preserve data distribution. 
- **Impact:** 
  - Rows affected: 6,053 rows for age, 5,759 rows for gender, 6,026 rows for year, 6,143 rows for population, and 6,117 rows for income_groups were affected.
  - Also minimal effect on data distribution.

### Issue 3: Income Groups Typos and Conversion
- **Cleaning Method:** Fixed typos in the income_groups column by mapping erroneous categories to correct ones and converted them into numeric categories with labels.
- **Implementation:**
  ```python
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

  df_cleaned['income_groups'].replace(income_group_mapping, inplace=True)
  df_cleaned['income_groups'] = df_cleaned['income_groups'].astype('category').cat.rename_categories({
    1: 'Low Income',
    2: 'Lower Middle Income',
    3: 'Upper Middle Income',
    4: 'High Income',
    99: 'Unknown'
  })
  ```
- **Justification:** Using replace() to correct typos and then converting income_groups to a categorical data type permitted efficient and scalable data cleaning.
- **Impact:** 
  - Rows affected: All rows converted to numeric categories.
  - Column was successfully converted to numeric categories, allowing for meaningful comparisons across income levels.

### Issue 4: Gender Column Conversion
- **Cleaning Method:** Converted the gender column to a categorical variable with specific labels for each category.
- **Implementation:**
  ```python
  df_cleaned['gender'] = df_cleaned['gender'].astype('category').cat.rename_categories({
    1: '1 (Male?)',
    2: '2 (Female?)',
    3: '3 (Other?)',
    99: 'Unknown'
  })
  ```
- **Justification:** Converting gender to categorical with clear labels improved data interpretation, particularly given the presence of non-binary or unknown gender values.
- **Impact:** 
  - Rows affected: All rows converted to numeric categories.
  - Clearer categorical interpretation.

### Issue 5: Year Column
- **Cleaning Method:** Corrected future years by assuming typos: if year is between 2025 and 2099, changed to 19XX (e.g., 2025 -> 1925); if year is greater than or equal to 2100, changed to 20XX (e.g., 2119 -> 2019).
- **Implementation:**
  ```python
  df_cleaned['year'] = df_cleaned['year'].apply(lambda x: x - 100 if 2025 <= x <= 2099 else x)
  df_cleaned['year'] = df_cleaned['year'].apply(lambda x: x - 100 if x >= 2100 else x)
  ```
- **Justification:** The most plausible explanation for years in the 2025-2099 range is that they should represent years in the 1900s. Similarly, years 2100 and beyond are likely intended to be in the 2000s. The use of .apply() allows row-by-row application of logic to correct the year. 
- **Impact:** 
  - Rows affected: 64,810 rows.
  - The maximum year changed from 2119 to 2024, and the median year shifted from 2025 to 1973, reflecting the correction of future dates.

## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv (or whatever you named it)
- **Rows**: 122,768 entries (after removing duplicates)
- **Columns**: 5 columns

### Column Details
| Column Name   | Data Type | Non-Null Count | Unique Values | Mean/Mode Value          |
|---------------|-----------|----------------|---------------|--------------------------|
| income_groups | category  | 122,768        | 5             | Mode: 'Low Income'        |
| age           | float64   | 122,768        | 101           | Mean: 49.99               |
| gender        | category  | 122,768        | 4             | Mode: '1 (Male?)'         |
| year          | float64   | 122,768        | 100           | Median: 1973              |
| population    | float64   | 122,768        | 98            | Median: 7.14M             |

### Summary of Changes
- Removed 2,950 duplicate rows.
- Imputed missing values for `income_groups`, `age`, `gender`, `year`, and `population`.
- Corrected typos in `income_groups`, mapped them to numeric categories, and labeled them appropriately.
- Converted `gender` to categorical with labeled categories, including an "Unknown" category for missing data.
- Fixed erroneous year values for rows with future years.

### Final Data Distribution Comparison
- Data distribution remained largely consistent after cleaning, with the exception of the year column where future values were corrected. 
