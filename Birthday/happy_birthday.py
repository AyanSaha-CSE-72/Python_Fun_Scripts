import pygame
import time
import os
import random
from colorama import init, Fore, Style

# Initialize colorama and pygame mixer
init(autoreset=True)
pygame.init()
pygame.mixer.init()

# Load and play happy birthday music (loop indefinitely)
pygame.mixer.music.load("happy_birthday.mp3")  # Put your mp3 file here
pygame.mixer.music.play(-1)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_sayed_banner():
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "🎉🎉🎉 Happy Birthday, Sayed! 🎉🎉🎉\n")
    print(Fore.CYAN + "Wishing you a fantastic day filled with joy and surprises!\n")
    print(Fore.GREEN + "     🕯️   🎂   🎁   🎉   🥳   🌟   🎊   🍰\n")

def confetti_burst(duration=2, width=50, height=12):
    symbols = ['*', '+', '×', '•', '★', '☆', '✦', '✧']
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTBLUE_EX]
    end_time = time.time() + duration
    while time.time() < end_time:
        clear()
        for _ in range(height):
            line = ''.join(random.choice(colors) + random.choice(symbols) + ' ' for _ in range(width))
            print(line)
        time.sleep(0.15)

def balloon_fly():
    balloons = ["🎈", "🎈", "🎈", "🎈", "🎈"]
    for i in range(12):
        clear()
        print("\n" * (12 - i))
        print("   ".join(balloons))
        print(Fore.LIGHTGREEN_EX + "🎉🎉🎉 Happy Birthday, Sayed! 🎉")
        print(Fore.CYAN + "Wishing you a fantastic day filled with joy and surprises!\n")
        print(Fore.MAGENTA + "🧑‍🦰SAYED! 🎉")
        time.sleep(0.3)


# Your animated hearts function
def animated_hearts():
    hearts = ['❤️ ', '💛 ', '💚 ', '💙 ', '💜 ', '🧡 ']
    for i in range(10):
        clear()
        print("\n\n")
        print("   " + "".join([hearts[(i+j)%len(hearts)] for j in range(10)]))
        print("       🎈 Happy Birthday Sayed! 🎈")
        print("   " + "".join([hearts[(i-j)%len(hearts)] for j in range(10)]))
        time.sleep(0.3)

def show_cake_image(path="cake.png"):
    print("Opening Pygame window to show the cake image...")
    try:
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Happy Birthday Cake 🎂")

        cake_img = pygame.image.load(path)
        cake_img = pygame.transform.scale(cake_img, (400, 300))
        print(f"Loaded image '{path}' successfully.")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((255, 255, 255))
            screen.blit(cake_img, (0, 0))
            pygame.display.flip()
    except pygame.error as e:
        print(f"Error loading cake image: {e}")
        input("Press Enter to exit...")
    finally:
        print("Closing Pygame and stopping music.")
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    clear()
    show_sayed_banner()
    confetti_burst()
    time.sleep(1)
    balloon_fly()

    # Add the animated hearts here
    animated_hearts()

    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "\n\n    From your friend 💙 — Ayan💻🐍")
    input(Fore.WHITE + "\n\nPress Enter to see the cake and exit...")

    show_cake_image()  # Ensure cake.png is in the same folder
