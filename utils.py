"""
Utility functions for the Dog Pet Care Chatbot.
"""

import os
import sys
import time
import random

# ANSI color codes
COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m"
}

def clear_screen():
    """Clear the terminal screen."""
    print('\033c', end='')

def print_colored(text, color="white"):
    """
    Print text in the specified color.
    
    Args:
        text (str): The text to print
        color (str): The color to use
    """
    if color in COLORS:
        print(f"{COLORS[color]}{text}{COLORS['reset']}")
    else:
        print(text)

def print_typing_effect(text, min_delay=0.01, max_delay=0.05):
    """
    Print text with a typing effect.
    
    Args:
        text (str): The text to print
        min_delay (float): Minimum delay between characters
        max_delay (float): Maximum delay between characters
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        # Vary the typing speed to make it more realistic
        delay = random.uniform(min_delay, max_delay)
        # Add larger pauses after sentence endings
        if char in ['.', '!', '?', '\n']:
            delay = delay * 3
        time.sleep(delay)
    print()

def print_header():
    """Print the chatbot header with ASCII art."""
    header = r"""
    ╔═══════════════════════════════════════════════╗
    ║                                               ║
    ║   🐕  DOG PET CARE CHATBOT  🐾                ║
    ║                                               ║
    ║   Your friendly assistant for all dog care    ║
    ║   questions and advice!                       ║
    ║                                               ║
    ╚═══════════════════════════════════════════════╝
    """
    print_colored(header, "cyan")
