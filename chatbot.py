
import json
import random
import re
from knowledge_base import KnowledgeBase
from utils import print_colored

class DogCareBot:
    def __init__(self):
        """Initialize the dog care chatbot with its knowledge base."""
        self.knowledge_base = KnowledgeBase()
        self.conversation_history = []
        self.current_context = None
        self.load_responses()
        
    def load_responses(self):
        """Load response templates from the knowledge base."""
        self.greetings = self.knowledge_base.get_data('general_responses')['greetings']
        self.farewells = self.knowledge_base.get_data('general_responses')['farewells']
        self.fallbacks = self.knowledge_base.get_data('general_responses')['fallbacks']
        
    def process_query(self, query):
        """
        Process the user's query and generate an appropriate response.
        
        Args:
            query (str): The user's input text
            
        Returns:
            str: The chatbot's response
        """
        # Convert to lowercase for easier processing
        query = query.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append(query)
        
        # Handle help command
        if query == 'help':
            return self._show_help()
            
        # Handle greeting
        if self._is_greeting(query):
            return random.choice(self.greetings)
            
        # Handle categories command
        if query == 'categories':
            return self._list_categories()
            
        # Handle breed information
        breed_match = re.search(r'(information|info|facts|about)\s+(\w+)\s+breed', query)
        if breed_match:
            breed = breed_match.group(2)
            return self._get_breed_info(breed)
            
        # Check for category-specific queries
        for category in self.knowledge_base.get_categories():
            if category.lower() in query:
                self.current_context = category
                return self._get_category_info(category)
        
        # Check for topics within the current context
        if self.current_context:
            context_data = self.knowledge_base.get_data(self.current_context)
            for topic, info in context_data.items():
                if topic in query:
                    return info
        
        # Use keyword matching for specific topics
        response = self._keyword_matching(query)
        if response:
            return response
            
        # If we reach here, we don't have a specific answer
        return random.choice(self.fallbacks)
    
    def _is_greeting(self, text):
        """Check if the text is a greeting."""
        greetings = ['hello', 'hi', 'hey', 'greetings', 'howdy']
        return any(word in text for word in greetings)
    
    def _keyword_matching(self, query):
        """Match keywords in the query to knowledge base entries."""
        # Important health concerns should be prioritized
        emergency_keywords = ['emergency', 'poison', 'ate', 'vomit', 'diarrhea', 
                             'not eating', 'bleeding', 'blood', 'injury', 'hurt']
        
        if any(keyword in query for keyword in emergency_keywords):
            return self.knowledge_base.get_data('emergency')['general_advice']
            
        # Check for food related questions
        food_keywords = ['food', 'feed', 'feeding', 'diet', 'nutrition', 'eat']
        if any(keyword in query for keyword in food_keywords):
            return self._get_category_info('feeding')
            
        # Check for training related questions
        training_keywords = ['train', 'training', 'command', 'teach', 'behavior']
        if any(keyword in query for keyword in training_keywords):
            return self._get_category_info('training')
            
        # Check for health related questions
        health_keywords = ['health', 'vet', 'veterinarian', 'sick', 'vaccine', 'medicine']
        if any(keyword in query for keyword in health_keywords):
            return self._get_category_info('health')
            
        # Check for grooming related questions
        grooming_keywords = ['groom', 'grooming', 'bath', 'nail', 'fur', 'hair', 'brush']
        if any(keyword in query for keyword in grooming_keywords):
            return self._get_category_info('grooming')
            
        return None
    
    def _show_help(self):
        """Display help information."""
        help_text = """
Here are some commands and questions you can ask:

Commands:
- 'categories' - List all available categories
- 'help' - Show this help message
- 'exit' - Exit the chatbot

Example questions:
- "How often should I feed my dog?"
- "What's the best way to train a puppy?"
- "Tell me about health issues in dogs"
- "How do I groom my dog properly?"
- "Information about Labrador breed"
- "What should I do in case of an emergency?"

You can also ask specific questions about feeding, training, 
grooming, health, exercise, or any other dog care topic!
"""
        return help_text
    
    def _list_categories(self):
        """List all available categories in the knowledge base."""
        categories = self.knowledge_base.get_categories()
        category_list = "\n".join([f"- {category}" for category in categories])
        return f"Here are the available categories of dog care information:\n\n{category_list}\n\nAsk me about any of these topics!"
    
    def _get_category_info(self, category):
        """Get general information about a category."""
        try:
            # Set the context to this category for follow-up questions
            self.current_context = category
            
            # Get information from the knowledge base
            category_data = self.knowledge_base.get_data(category)
            
            if 'overview' in category_data:
                return category_data['overview']
            
            # If no overview, create a summary of topics
            topics = list(category_data.keys())
            topics_list = "\n".join([f"- {topic}" for topic in topics])
            
            return f"Here's what I know about {category}:\n\n{topics_list}\n\nAsk me about any of these specific topics!"
        except:
            return f"I don't have information about {category} at the moment."
    
    def _get_breed_info(self, breed):
        """Get information about a specific dog breed."""
        try:
            breeds_data = self.knowledge_base.get_data('breeds')
            # Try to find the breed (case insensitive)
            for known_breed, info in breeds_data.items():
                if known_breed.lower() == breed.lower():
                    return f"Information about {known_breed}:\n\n{info}"
            
            return f"I don't have specific information about the {breed} breed. Consider asking your veterinarian or a professional dog breeder."
        except:
            return "I couldn't retrieve breed information at the moment."
