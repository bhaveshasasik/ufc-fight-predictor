## Data Cleansing/EDA

**Started with the CSV files:**
- **UFC top fighters:** Top fighters in the UFC.
- **UFC all fights:** Includes all UFC fights since 1993 and all of the statistics associated with the fight, including attributes such as avg. KO, avg. total strikes landed, avg. takedowns per fight, etc.
- **UFC fighter statistics:** All of the statistics of the current and legends in the UFC, including attributes such as wins, losses, height, weight, reach, stance, etc.

### Data Cleansing
- Turned all CSVs into dataframes.
- Filtered the UFC fights CSV and their respective statistics to only include the fights with the top UFC fighters to eliminate excess noise in the data.
- Repeated this process with the UFC fighter statistics, only including the top fighters.
- Dropped unnecessary features such as nickname, hometown, etc., to improve model fit and increase training speed.
- Merged these fight statistics into a dataset, including both all the fight statistics along with the respective fighter statistics, resulting in our final dataset used for the model.

## Model Building Methodology
We explored a variety of models to use so that we could hone in on the best one. After evaluating each model, we decided to use a Random Forest Model based on its accuracy and precision. We started with 30+ features and used a variety of statistical methods to focus on a few key predictors. We also implemented grid search to find the optimal hyperparameters.

- Scaled data and fitted to each specific fighter to avoid dimensionality issues.
- Implemented logic to attribute features to their respective fighters' names.

## Front End Implementation
We call an instance of the model object and integrated it seamlessly into our Streamlit frontend for users to easily adjust fighter attributes and have fun with the tool.
