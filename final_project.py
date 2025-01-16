import csv
import random

#reads all data from csv into an array
def read_data_from_csv(filename):
    try:
        data = []
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

# counts data by creating a dictionary and iterating over each column and row
#stores the column data and adds a count if its not the first time its been read
#if its the first time it sets the count to 1
def get_counts(data):
    count = {}
    headers = data[0]
    num_of_cols = len(headers)
    for header in headers:
        count[header] = {}
    for col in range(num_of_cols):
        name_of_col = headers[col]
        column_data = count[name_of_col]
        for row in range(1,len(data)):
            value = data[row][col]
            if value in column_data:
                column_data[value] += 1
            else:
                column_data[value] = 1
    return count


#generates synthetic data by determining the probability of a value and throwing it into
#the random choices function
def generate_synthetic_data(counted_data, num_people):
    synthetic_data = {}
    for key, counts in counted_data.items():
        values = list(counts.keys())
        counts_list = list(counts.values())
        total_counts = sum(counts_list)
        item_prob = [count/total_counts for count in counts_list]
        synthetic_data[key] = random.choices(values, item_prob, k=num_people)
    return synthetic_data


#gets num of people to generate grades for with input validation to prevent user stupidity
def get_num_people():
     while True:
        try:
            num_people = int(input("How many people would you like to generate data for? "))
            if num_people > 0:
                return num_people
            else:
                print("Can't have negative amount of people")
        except ValueError:
            print("Invalid input. Positive integers only please.")

#write synthetic data to a csv file by first writing the headers(key) and then the data          
def write_synthetic_data_to_csv(filename, synthetic_data):
    try:
        with open(filename, 'w', newline = '') as file:
            w = csv.writer(file)
            w.writerow(synthetic_data.keys())
            for row in zip(*synthetic_data.values()):
                w.writerow(row)
            print(f"Synthetic data has been written to {filename}")
    except Exception as e:
        print(f"An error occured: {e}")
    
#main function that calls the read file fucntion and stores it in a list which is
#then used to get counts of all data for every header in the get_counts method
#calls the get num_people method and throws it into the synthetic data generator method
#lastly calls the write method to write the synthetic data to a new csv file        
def main():    
    data = read_data_from_csv("Fictional_Customers.csv")
##    print(data)
##    print('\n')
    counted_data = get_counts(data)
##    for key, counts in counted_data.items():
##        print(f"{key}:")
##        for value, count in counts.items():
##            print(f"\t{value} Count: {count}")
##        print('\n')
    num_people = get_num_people()
    synthetic_data = generate_synthetic_data(counted_data, num_people)
##    print('\n')
##    print(synthetic_data)
    write_synthetic_data_to_csv("synthetic_data.csv", synthetic_data)


if __name__ == "__main__":
    main()
