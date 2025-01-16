import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
import matplotlib.pyplot as plt

from backend_operations import DatabaseHandler, DataProcessor
from tabulate import tabulate

def select_file():
    """Opens a file dialog to select a CSV or Excel file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("CSV and Excel files", "*.csv *.xlsx *.xls"),
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx *.xls")
        ]
    )
    return file_path

def select_save_file(default_ext=".csv"):
    """Opens a file dialog to select a save location."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=default_ext,
        filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("All files", "*.*")
        ]
    )
    return file_path

def main():
    """Main function to run the user interface."""
    db_handler = DatabaseHandler()
    data_processor = DataProcessor()

    while True:
        print("\n--- Baseball Wins Predictor Pro ---")
        print("1. Load data from CSV or XLS or XLSX")
        print("2. Display all records")
        print("3. Add a new record")
        print("4. Update an existing record")
        print("5. Delete a record")
        print("6. Analyze yearly team statistics")
        print("7. Predict wins")
        print("8. Create Data Visualizations")
        print("9. Export Database")
        print("10. Exit")
        
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                file_path = select_file()
                if file_path:
                    try:
                        db_handler.load_data_from_file(file_path)
                        print("Data loaded successfully!")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("No file selected.")
            
            elif choice == "2":
                records, headers = db_handler.read_records()
                if not records:
                    print("No records to display.")
                else:
                    print("\n--- Baseball Stats ---")
                    print(tabulate(records, headers=headers, tablefmt="pretty"))
            
            elif choice == "3":
                try:
                    print("Enter the new record data:")
                    team = input("Team: ")
                    year = int(input("Year: "))
                    wins = int(input("Wins: "))
                    losses = int(input("Losses: "))
                    runs_scored = int(input("Runs Scored: "))
                    runs_allowed = int(input("Runs Allowed: "))
                    home_runs = input("Home Runs (optional, press Enter to skip): ")
                    era = input("ERA (optional, press Enter to skip): ")
                    
                    # Prepare the record with optional fields handled properly
                    record = (
                        team,
                        year,
                        wins,
                        losses,
                        runs_scored,
                        runs_allowed,
                        int(home_runs) if home_runs.strip() else None,
                        float(era) if era.strip() else None,
                    )
                    
                    # Add the record to the database
                    db_handler.add_record(record)
                    print("Record added successfully!")
                except ValueError as ve:
                    print(f"Input Error: {ve}")
                except Exception as e:
                    print(f"An error occurred: {e}")

            
            elif choice == "4":
                try:
                    record_id = int(input("Enter the record ID to update: "))
                    print("Enter updated data (press Enter to skip a field):")
                    
                    updated_data = {}
                    
                    team = input("Team: ")
                    if team.strip():
                        updated_data["team"] = team

                    year = input("Year: ")
                    if year.strip():
                        updated_data["year"] = int(year)

                    wins = input("Wins: ")
                    if wins.strip():
                        updated_data["wins"] = int(wins)

                    losses = input("Losses: ")
                    if losses.strip():
                        updated_data["losses"] = int(losses)

                    runs_scored = input("Runs Scored: ")
                    if runs_scored.strip():
                        updated_data["runs_scored"] = int(runs_scored)

                    runs_allowed = input("Runs Allowed: ")
                    if runs_allowed.strip():
                        updated_data["runs_allowed"] = int(runs_allowed)

                    home_runs = input("Home Runs (optional, press Enter to skip): ")
                    if home_runs.strip():
                        updated_data["home_runs"] = int(home_runs)

                    era = input("ERA (optional, press Enter to skip): ")
                    if era.strip():
                        updated_data["era"] = float(era)
                    
                    # Update the record in the database
                    db_handler.update_record(record_id, updated_data)
                    print(f"Record with ID {record_id} updated successfully!")
                except ValueError as ve:
                    print(f"Input Error: {ve}")
                except Exception as e:
                    print(f"An error occurred: {e}")

            
            
            elif choice == "5":
                record_id = int(input("Enter the record ID to delete: "))
                db_handler.delete_record(record_id)
            
            elif choice == "6":
                criteria = input("Enter filtering criteria (e.g., 'wins > 80'): ")
                filtered_data = data_processor.filter_data(criteria)
                print("\n--- Filtered Data ---")
                print(filtered_data)
            
            elif choice == "7":
                # Predict wins dynamically
                try:
                    # Load all records into a DataFrame
                    records, headers = db_handler.read_records()
                    if not records:
                        raise ValueError("No data available in the database for prediction.")
                    
                    df = pd.DataFrame(records, columns=headers)
                    
                    # Check if the target column exists
                    if "wins" not in df.columns:
                        raise ValueError("The target column 'wins' is missing in the dataset.")
                    # Call the prediction function
                    predictions, mse, r2 = data_processor.predict_wins_dynamic(df)
                    
                    print("\n--- Predictions Complete ---")
                    print(f"Predictions: {predictions}")
                    print(f"Mean Squared Error: {mse:.2f}")
                    print(f"R^2 Score: {r2:.2f}")
                except ValueError as ve:
                    print(f"Validation Error: {ve}")
                except Exception as e:
                    print(f"Error during prediction: {e}")

            elif choice == "8":
                try:
                    data_processor.create_visualizations()
                    print("Visualizations have been saved. Check baseball_stats_visualization.png")
                except Exception as e:
                    print(f"Visualization Error: {e}")
            
            elif choice == "9":
                export_path = select_save_file()
                if export_path:
                    try:
                        db_handler.export_data(export_path)
                        print(f"Data exported to {export_path}")
                    except Exception as e:
                        print(f"Export Error: {e}")
            
            elif choice == "10":
                print("Exiting... Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
