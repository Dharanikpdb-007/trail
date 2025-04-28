"""
Knowledge base module for the Dog Pet Care Chatbot.
Manages the loading and retrieval of information from JSON data files.
"""

import json
import os

class KnowledgeBase:
    def __init__(self):
        """Initialize the knowledge base by loading data from JSON files."""
        self.data = {}
        self.load_data()
    
    def load_data(self):
        """Load all the knowledge base data from JSON files."""
        # Load primary knowledge base
        with open('dog_care_data.json', 'r') as file:
            self.data = json.load(file)
            
    def get_data(self, category):
        """
        Retrieve data for a specific category.
        
        Args:
            category (str): The category to retrieve
            
        Returns:
            dict: The data for the specified category
        """
        if category in self.data:
            return self.data[category]
        return {"overview": "I don't have information about this category yet."}
    
    def get_categories(self):
        """
        Get a list of all available categories.
        
        Returns:
            list: A list of category names
        """
        # Filter out utility categories
        main_categories = [cat for cat in self.data.keys() 
                          if cat not in ['general_responses', 'breeds']]
        return main_categories
    
    def search(self, query):
        """
        Search the knowledge base for information related to the query.
        
        Args:
            query (str): The search query
            
        Returns:
            list: A list of relevant information
        """
        results = []
        query = query.lower()
        
        # Search through all categories
        for category, category_data in self.data.items():
            # Skip utility categories for generic searches
            if category in ['general_responses']:
                continue
                
            # If category is dictionary, search through its keys and values
            if isinstance(category_data, dict):
                for key, value in category_data.items():
                    if query in key.lower() or (isinstance(value, str) and query in value.lower()):
                        results.append({
                            "category": category,
                            "topic": key,
                            "info": value
                        })
        
        return results
