#import random to be able to generate random numbers
import random

#generate the random integer in specific range based on the difficulty the user selects
def generate_number(difficulty):
    if difficulty == "easy":
        return random.randint(1,10)
    elif difficulty == "medium":
        return random.randint(1,50)
    else:
        return random.randint(1,100)
    
#get the users guess and validate that it is a valid integer and in range for the difficulty level selected
def get_user_guess(difficulty):
    if difficulty == "easy":
        lower, upper = 1, 10
        print(f"Guess a number between {lower} and {upper} please.")
    elif difficulty == "medium":
        lower, upper = 1, 50
        print(f"Guess a number between {lower} and {upper} please.")
    else:
        lower, upper = 1, 100
        print(f"Guess a number between {lower} and {upper} please.")
    while True:
        try:
            guess = int(input("Enter guess: "))
            if lower <= guess <= upper:
                return guess
            else:
                print(f"Your guess should be in range {lower},{upper}")
        except ValueError:
            print("Invalid input. Please enter a valid integer")
            
#check the guess against the number generated and return a message based on the comparison
def check_guess(guess, target):
    if guess < target:
        return "Too low!"
    elif guess > target:
        return "Too high!"
    else:
        return "Congratulations! You guessed it!"

#check the guess against the number generated and return a hint based on the comparison 
def display_hint(guess, target):
    if guess < target:
        print("Hint: Try a number higher.")
    elif guess > target:
        print("Hint: Try a number lower.")
              
#generate a score with different bases based on difficulty to reward users more points for greater difficulty
def calculate_score(attempts, difficulty):
    if difficulty == "easy":
        base_score = 100
    elif difficulty == "medium":
        base_score = 150
    else:
        base_score = 200
    final_score = base_score - (attempts * 10)
    return final_score

#call all the game functions in a loop that breaks if the user does not want to play again
#within main game loop allow the user to guess until they guess correctly or run out of attempts
def main():
    print("Welcome to the Guessing Game!")
    while True:
        difficulty = input("Choose difficulty: easy, medium, or hard? ").lower()
        if difficulty not in ["easy", "medium", "hard"]:
            print("Invalid Choice. Please try again. ")
            continue
        target = generate_number(difficulty)
        attempts = 0
        while True:
            guess = get_user_guess(difficulty)
            attempts = attempts + 1
            if guess == target:
                print("Congratulations! You guessed it!")
                print(f"Your score is: {calculate_score(attempts, difficulty)}")
                break
            else:
                print(check_guess(guess,target))
                display_hint(guess, target)
            if difficulty == "easy":
                continue
            elif difficulty == "medium" and attempts > 9:
                print ("Better luck next time, you are out of attempts. ")
                break
            elif difficulty == "hard" and attempts > 4:
                print ("Better luck next time, you are out of attempts. ")
                break
        play_again = input("Would you like to play again? yes or no ").lower()
        if play_again != "yes":
            break
        
main()   
