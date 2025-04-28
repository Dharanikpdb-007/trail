#!/usr/bin/env python3
"""
Main entry point for the Dog Pet Care Chatbot.
This file handles the user interface and interaction loop.
"""

import json
import os
import time
from chatbot import DogCareBot
from utils import clear_screen, print_colored, print_header, print_typing_effect

def main():
    """Main function to run the dog pet care chatbot."""
    clear_screen()
    print_header()
    
    # Initialize the chatbot
    bot = DogCareBot()
    
    # Welcome message
    print_colored("\nWelcome to the Dog Pet Care Assistant!", "cyan")
    print_colored("I can help you with questions about caring for your dog.", "cyan")
    print_colored("Type 'help' to see available commands or 'exit' to quit.\n", "cyan")
    
    # Main interaction loop
    while True:
        try:
            user_input = input("\n🐾 You: ")
            
            # Exit command
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print_colored("\nThank you for using Dog Pet Care Assistant! Woof goodbye! 🐕", "cyan")
                break
                
            # Handle empty input
            if not user_input.strip():
                print_colored("Please type something or 'exit' to quit.", "yellow")
                continue
                
            # Process user input and get response
            print("\n🤖 Assistant: ", end="")
            print_typing_effect(bot.process_query(user_input))
            
        except KeyboardInterrupt:
            print_colored("\n\nExiting Dog Pet Care Assistant. Have a great day! 🐕", "cyan")
            break
        except Exception as e:
            print_colored(f"\nOops! Something went wrong: {str(e)}", "red")
            print_colored("Let's continue our conversation.", "yellow")

if __name__ == "__main__":
    main()
