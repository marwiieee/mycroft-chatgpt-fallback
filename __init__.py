# Import necessary libraries
from mycroft import FallbackSkill # Provides fallback functionality for the skill
import openai as ai # Handles the interaction with the OpenAI API

# Define the OpenAI model to use
MODEL = "gpt-3.5-turbo"

# Define the ChatGPT skill as a subclass of FallbackSkill
class FallbackChatgpt(FallbackSkill):
    
    # Initialize the ChatGPT skill
    def __init__(self):
        super().__init__() # Initialize the parent class
        self._chat = None # Initialize the chat attribute to None
        self.key = self.settings.get("key") # Retrieve the OpenAI API key from the settings

        self.initialize() # Call the initialize method to register the fallback method

    # Register the handle_fallback_ChatGPT method as a fallback method
    def initialize(self):
        self.register_fallback(self.handle_fallback_ChatGPT, 8) # Set the fallback priority to 8

    # Handle the fallback method using the OpenAI Chat API
    def handle_fallback_ChatGPT(self, message):
        prompt = [{"role": "user", "content": message.data['utterance']}] # Create a prompt for the OpenAI Chat API
        self.log.info(f"Prompt: {prompt}") # Log the prompt to the console

        try:
            # Generate a response using the OpenAI Chat API
            completion = self.chatgpt.create(model=MODEL, messages=prompt, max_tokens=200)
            response = completion.choices[0].message["content"].strip("?_") # Extract the response from the API and strip trailing question marks and underscores

            # Speak the response and return True to indicate success
            if response:
                self.log.info(f"Response: {response}") # Log the response to the console
                self.speak(response)
                return True
            else:
                return False # Return False if the response is empty
        except Exception as e:
            self.log.error(f"Error in ChatGPT fallback request: {e}") # Log the error to the console
            return False # Return False if an error occurs

    # Instantiate the ChatCompletion class and store it in the _chat attribute
    @property
    def chatgpt(self):
        if not self.key:
            raise ValueError("OpenAI key not set in settings.json")
        if not self._chat:
            ai.api_key = self.key
            self._chat = ai.ChatCompletion
        return self._chat


# Create a new instance of the ChatGPT skill
def create_skill():
    return FallbackChatgpt()


# Run the fallback method with a sample message if the script is run directly
if __name__ == "__main__":
    from ovos_utils.messagebus import Message

    gpt = FallbackChatgpt()
    msg = Message("intent_failure", {"utterance": "when will the world end?"})
    gpt.handle_fallback_ChatGPT(msg)
