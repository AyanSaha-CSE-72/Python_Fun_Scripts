import time
import sys

lyrics = [
    "So I'ma love you every night like it's the last night",
    "Like it's the last night",
    "If the world was ending",
    "I'd wanna be next to you",
    "If the party was over",
    "And our time on Earth was through",
    "I'd wanna hold you just for a while",
    "And die with a smile",
    "If the world was ending",
    "I'd wanna be next to you",
    "Right next to you"
]

delays = [0.6, 0.7, 1.0, 4.6, 1.0, 3.6, 1.7, 2.0, 0.9, 1.3, 1.0]  

def print_lyrics():
    for i, line in enumerate(lyrics):
        for char in line:
            print(char, end='')
            sys.stdout.flush()
            time.sleep(0.05)  
        print()
        time.sleep(delays[i])

print_lyrics()