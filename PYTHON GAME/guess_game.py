import random

def guess_the_number():
    print("Welcome to Guess the Number!")
    print("I'm thinking of a number between 1 and 100.")
    
    number = random.randint(1, 100)
    attempts = 0
    
    while True:
        try:
            guess = int(input("Take a guess: "))
            attempts += 1
            
            if guess < number:
                print("Too low! Try again.")
            elif guess > number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed it in {attempts} tries.")
                break
                
        except ValueError:
            print("Oops! Please enter a valid number.")

if __name__ == "__main__":
    guess_the_number()
