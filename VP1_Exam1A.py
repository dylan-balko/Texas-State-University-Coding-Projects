#import random function from python library to be able to generate randoms
import random

#read every name from the input file
#error handling for if the file doesn't exist and any other errors that may pop up
def read_names_from_file(filename):
    try:
        with open(filename, 'r') as file:
            names = [str(line.strip()) for line in file]
            return names
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occured: {e}")


#asks user for amount of grades per student and validates that it is a postive integer
def get_num_grades():
    while True:
        try:
            num_grades = int(input("How many grades per student? "))
            if num_grades > 0:
                return num_grades
            else:
                print("Can't have negative amount of grades for students.")
        except ValueError:
            print("Invalid input. Positive integers only please.")

        
#call the read name function to write grades randomly generated for each name
#number of grades randomly generated is based on user input
#basic error handling        
def write_grades_to_file(filename,num_grades):
    try:
        with open(filename, 'w') as file:
            names = read_names_from_file("name_input.txt")
            for name in names:
                grades = [random.randint(1,100) for _ in range(int(num_grades))]
                file.write(f"{name}: {str(grades)}\n")
            print(f"Grades have successfully been written to {filename}")        
    except Exception as e:
        print(f"An error occured: {e}")

        
#reads each line and displays the total number of grades
#does this by spliting each line after the name which is ended with ':' and stripping
#the list brackets and comma seperators in between each grade to extract just the grade
#after total grades is printed it reads each line prints it and moves onto the next
#for every line in the file
def read_and_display_total_from_file(filename):
    try:
        with open(filename, 'r') as file:
            total = 0
            for line in file:
                grades_str = line.split(":")[1].strip()
                grades = [int(grade.strip()) for grade in grades_str.strip("[]").split(",")]
                total += sum(grades)
            print(f"\nTotal is: {total}")
            print("\n")
            file.seek(0)
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occured: {e}")


#main function that sets the output file name and calls
#the write function, get number of grades function, and read/total function
def main():
    filename = "grades_(total).txt"
    num_grades = get_num_grades()
    write_grades_to_file(filename,num_grades)
    read_and_display_total_from_file(filename)
    
   
        
main()
    
    
