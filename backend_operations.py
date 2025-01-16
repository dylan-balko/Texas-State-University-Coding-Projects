import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

class DatabaseHandler:
    def __init__(self, db_name="baseball.db"):
        """Initialize the database connection with optional database name."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the baseball stats table with comprehensive columns."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS baseball_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team TEXT NOT NULL,
                year INTEGER NOT NULL,
                wins INTEGER NOT NULL,
                losses INTEGER NOT NULL,
                runs_scored INTEGER NOT NULL,
                runs_allowed INTEGER NOT NULL,
                home_runs INTEGER,
                era REAL,
                win_percentage REAL,
                run_difference INTEGER
            )
        """)
        self.conn.commit()

    def _validate_data(self, df):
        """
        Validate input data with comprehensive checks.
        
        Args:
            df (pandas.DataFrame): Input DataFrame to validate
        
        Returns:
            pandas.DataFrame: Cleaned and validated DataFrame
        """
        # Required columns with type checks
        required_columns = {
            "team": str,
            "year": int,
            "wins": int,
            "losses": int,
            "runs_scored": int,
            "runs_allowed": int
        }
        
        # Optional columns
        optional_columns = {
            "home_runs": int,
            "era": float
        }
        
        # Check for missing required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Validate and convert column types
        for col, dtype in {**required_columns, **optional_columns}.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid data type for column {col}")
        
        # Additional data validations
        df['win_percentage'] = df['wins'] / (df['wins'] + df['losses'])
        df['run_difference'] = df['runs_scored'] - df['runs_allowed']
        
        # Remove rows with negative or unrealistic values
        df = df[df['wins'] >= 0]
        df = df[df['losses'] >= 0]
        df = df[df['runs_scored'] >= 0]
        df = df[df['runs_allowed'] >= 0]
        
        return df

    def load_data_from_file(self, file_path):
        """Load data from a CSV or Excel file into the database."""
        # Load the file based on extension
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
        # Clean string columns to remove unwanted spaces or characters
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].str.replace("\xa0", " ", regex=False).str.strip()
        
        # Required and optional columns for the database
        required_columns = ["team", "wins", "losses", "runs_scored", "runs_allowed", "year"]
        optional_columns = ["home_runs", "era"]
        
        # Display columns to the user for mapping
        print("\nColumns in your file:")
        for i, column in enumerate(df.columns):
            print(f"{i + 1}. {column}")
        
        # Map columns dynamically
        column_mapping = {}
        for col in required_columns:
            user_input = input(f"Enter the number corresponding to '{col}' in your file: ")
            column_index = int(user_input) - 1
            column_mapping[col] = df.columns[column_index]
        
        for col in optional_columns:
            user_input = input(f"Enter the number corresponding to '{col}' in your file (or press Enter to skip): ")
            if user_input.strip():
                column_index = int(user_input) - 1
                column_mapping[col] = df.columns[column_index]
            else:
                column_mapping[col] = None  # Mark as missing
        
        # Rename columns based on the mapping
        df.rename(columns={v: k for k, v in column_mapping.items() if v is not None}, inplace=True)
        
        # Handle missing optional columns
        for col in optional_columns:
            if column_mapping[col] is None:  # Set missing columns to None
                df[col] = None
        
        # Ensure the DataFrame has all required and optional columns
        df = df[required_columns + optional_columns]
        
        # Add calculated columns
        df['win_percentage'] = df['wins'] / (df['wins'] + df['losses'])
        df['run_difference'] = df['runs_scored'] - df['runs_allowed']
        
        # Load the data into the database
        df.to_sql("baseball_stats", self.conn, if_exists="replace", index=False)

    def read_records(self):
        """Retrieve all records and their headers from the database."""
        self.cursor.execute("SELECT * FROM baseball_stats")
        records = self.cursor.fetchall()
     # Dynamically fetch column names from the table schema
        self.cursor.execute("PRAGMA table_info(baseball_stats)")
        columns_info = self.cursor.fetchall()
        headers = [col[1] for col in columns_info]  # Extract column names
        return records, headers  # Return raw data and headers

    def add_record(self, record):
        """
        Add a new record to the database.

        Args:
            record (tuple): (team, year, wins, losses, runs_scored, runs_allowed, home_runs, era)
        """
        # Ensure the record contains at least the required columns
        if len(record) < 6:
            raise ValueError("Record must include at least team, year, wins, losses, runs_scored, and runs_allowed.")

        # Extract values from the record
        team = record[0]
        year = record[1]
        wins = record[2]
        losses = record[3]
        runs_scored = record[4]
        runs_allowed = record[5]
        home_runs = record[6] if len(record) > 6 else None
        era = record[7] if len(record) > 7 else None

        # Calculate derived columns
        win_percentage = wins / (wins + losses) if wins + losses > 0 else 0
        run_difference = runs_scored - runs_allowed

        # Insert the new record into the database
        self.cursor.execute("""
            INSERT INTO baseball_stats (team, year, wins, losses, runs_scored, runs_allowed, home_runs, era, win_percentage, run_difference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (team, year, wins, losses, runs_scored, runs_allowed, home_runs, era, win_percentage, run_difference))
        self.conn.commit()
        print("Record added successfully.")

    def update_record(self, record_id, updated_data):
        """
        Update a record in the database.

        Args:
            record_id (int): ID of the record to update.
            updated_data (dict): Dictionary of columns to update with their new values.
        """
        if not updated_data:
            raise ValueError("No data provided to update.")

        # Build the SQL query dynamically from the keys in updated_data
        update_query = ", ".join([f"{key} = ?" for key in updated_data.keys()])
        update_values = list(updated_data.values()) + [record_id]  # Add the record_id at the end

        # Execute the query
        self.cursor.execute(f"UPDATE baseball_stats SET {update_query} WHERE id = ?", update_values)
        self.conn.commit()
        print(f"Record with ID {record_id} updated successfully.")


    def delete_record(self, record_id):
        """Delete a record from the database."""
        try:
            # First, check if the record exists
            self.cursor.execute("SELECT rowid FROM baseball_stats WHERE rowid = ?", (record_id,))
            record = self.cursor.fetchone()
            
            if record is None:
                print(f"No record found with ID {record_id}")
                return
            
            # If record exists, proceed with deletion
            self.cursor.execute("DELETE FROM baseball_stats WHERE rowid = ?", (record_id,))
            self.conn.commit()
            print(f"Record with ID {record_id} deleted successfully.")
        
        except sqlite3.OperationalError as e:
            print(f"SQLite Error: {e}")
            
    def export_data(self, output_path):
        """Export database contents to CSV."""
        df = pd.read_sql_query("SELECT * FROM baseball_stats", self.conn)
        df.to_csv(output_path, index=False)
        print(f"Data exported to {output_path}")

class DataProcessor:
    def __init__(self, db_name="baseball.db"):
        """Initialize database connection."""
        self.conn = sqlite3.connect(db_name)

    def filter_data(self, criteria):
        """Filter data based on the given criteria."""
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)  # Optionally show all columns as well
        pd.set_option("display.width", 1000) 
        query = f"SELECT * FROM baseball_stats WHERE {criteria}"
        return pd.read_sql_query(query, self.conn)

    def create_visualizations(self, df=None):
        """Create multiple visualizations of baseball statistics."""
        if df is None:
            df = pd.read_sql_query("SELECT * FROM baseball_stats", self.conn)
        
        plt.figure(figsize=(15, 10))
        
        # 1. Wins Distribution
        plt.subplot(2, 2, 1)
        sns.histplot(df['wins'], kde=True)
        plt.title('Distribution of Team Wins')
        
        # 2. Win Percentage vs Run Difference
        plt.subplot(2, 2, 2)
        plt.scatter(df['run_difference'], df['win_percentage'])
        plt.title('Win Percentage vs Run Difference')
        plt.xlabel('Run Difference')
        plt.ylabel('Win Percentage')
        
        # 3. Team Performance Boxplot
        plt.subplot(2, 2, 3)
        sns.boxplot(x='team', y='wins', data=df)
        plt.title('Team Wins Comparison')
        plt.xticks(rotation=45)
        
        # 4. ERA vs Wins
        plt.subplot(2, 2, 4)
        plt.scatter(df['era'], df['wins'])
        plt.title('ERA vs Wins')
        plt.xlabel('ERA')
        plt.ylabel('Wins')
        
        plt.tight_layout()
        plt.savefig('baseball_stats_visualization.png')
        plt.close()
        
        print("Visualizations saved to baseball_stats_visualization.png")

    def predict_wins_dynamic(self, df, target_column="wins"):
        """
        Predict wins dynamically based on runs_scored, runs_allowed, and optionally home_runs/era.

        Parameters:
        - df (DataFrame): The dataset to use for prediction.
        - target_column (str): The name of the target column (default is "wins").

        Returns:
        - predictions (array): Predicted values for the test set.
        - mse (float): Mean squared error of the model.
        - r2 (float): R-squared score of the model.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input data must be a Pandas DataFrame.")

        # Mandatory features
        mandatory_features = ["runs_scored", "runs_allowed"]

        # Optional features (include only non-null rows for these)
        optional_features = ["home_runs", "era"]

        # Ensure mandatory features exist in the dataset
        missing_mandatory = [feature for feature in mandatory_features if feature not in df.columns]
        if missing_mandatory:
            raise ValueError(f"The dataset is missing mandatory features: {missing_mandatory}")

        # Validate the target column
        if target_column not in df.columns:
            raise ValueError(f"The target column '{target_column}' is missing in the dataset.")

        # Prepare feature list and drop rows with NaN in mandatory features
        X = df[mandatory_features].copy()
        y = df[target_column]
        X = X.dropna(subset=mandatory_features)  # Drop rows where mandatory features are missing
        y = y[X.index]  # Align target with filtered features

        for feature in optional_features:
            if feature in df.columns:
                # Create a copy of the feature column and ensure it's numeric
                temp_feature = pd.to_numeric(df[feature], errors='coerce')
                # Fill NaN values with 0 and explicitly convert to float
                temp_feature = temp_feature.fillna(0).astype(float)
                # Add the processed feature to X
                X[feature] = temp_feature

        # Ensure sufficient data remains
        if len(X) < 2:
            raise ValueError("Not enough data for training and testing.")

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Train the Linear Regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        predictions = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"\n--- Model Evaluation ---")
        print(f"Features used: {X.columns.tolist()}")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R^2 Score: {r2:.2f}")
        print(f"Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")

        return predictions, mse, r2
