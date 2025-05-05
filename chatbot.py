from openai import OpenAI

class DogCareBot:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []

    def process_query(self, query):
        self.conversation_history.append({"role": "user", "content": query})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": (
                        "You are a helpful and friendly dog care assistant. "
                        "Answer questions about feeding, training, health, grooming, emergencies, and dog breeds."
                    )},
                    *self.conversation_history
                ],
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply

        except Exception as e:
            return f"Sorry, something went wrong while contacting the AI: {str(e)}"
