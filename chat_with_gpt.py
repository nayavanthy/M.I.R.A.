from pymongo import MongoClient
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["MIRA"]
memory_collection = db["long_term_memory"]  # Stores persistent knowledge
short_term_memory = db["short_term_memory"]
chat_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SHORT_TERM_LIMIT = 10

# In-memory dictionary for Conversational Memory
conversational_memory = {}

def save_to_short_term(user_message, bot_response):
    """
    Saves user input and bot response to short-term memory.
    Deletes oldest records if exceeding SHORT_TERM_LIMIT.
    """
    short_term_memory.insert_one({"role": "user", "content": user_message})
    short_term_memory.insert_one({"role": "assistant", "content": bot_response})

    # Enforce memory limit by keeping only the last SHORT_TERM_LIMIT exchanges
    if short_term_memory.count_documents({}) > 2 * SHORT_TERM_LIMIT:
        oldest_entries = short_term_memory.find().sort("_id", 1).limit(2)  # Get two oldest
        for entry in oldest_entries:
            short_term_memory.delete_one({"_id": entry["_id"]})

def fetch_recent_conversation():
    """
    Retrieves the last SHORT_TERM_LIMIT messages to provide context to GPT.
    """
    recent_messages = list(short_term_memory.find().sort("_id", -1).limit(2 * SHORT_TERM_LIMIT))
    recent_messages.reverse()  # Ensure correct chronological order
    return [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]

def save_to_long_term_memory(user_input):
    """
    Saves structured data to long-term memory in MongoDB.
    If key already exists in a category, update it.
    """
    messages = [{"role": "system", "content": f"You are a helper function for an AI assistant."}]
    prompt = [{"role": "user", "content": f"""Structure the given input in the following manor so that it can be saved in a mondo db data base
               Example: 'my name is yogi' is the input. output expected is "{{"category":"personal", "key":"name", "value":"user's name is yogi"}}"
               Inputs may be of any type, choose a category and key accordingly
               Keep the JSON structure rigid and only give the JSON as response
               input statmenet- {user_input}"""}]
    
    messages.extend(prompt)

    response = chat_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    try:
        parsed_response = json.loads(response.choices[0].message.content.strip())
        memory_collection.update_one(
            {"category": parsed_response["category"], "key": parsed_response["key"]},
            {"$set": {"value": parsed_response["value"]}},
            upsert=True
        )
        print(f"saved {parsed_response["value"]} to memory")
    except json.JSONDecodeError:
        print("error saving to long term memory")

    

def fetch_long_term_memories(user_input):
    """
    Retrieves relevant long-term memories from MongoDB based on keywords in user input.
    """
    keywords = user_input.lower().split()
    memories = []

    for word in keywords:
        results = memory_collection.find({"value": {"$regex": word, "$options": "i"}})  # Case-insensitive search
        for memory in results:
            memory_text = f"{memory['category'].capitalize()} ({memory['key']}): {memory['value']}"
            if memory_text not in memories:
                memories.append(memory_text)

    return "\n".join(memories[:5])  # Return up to 5 relevant memories

def is_input_important(user_input):
    messages = [{"role": "system", "content": f"You are a helper function for an AI assistant."}]
    prompt = [{"role": "user", "content": f"""is there anything important in the input that needs to be saved for longterm use. 
               Example: names of people, goals, likes, dislikes, habits, possesions etc. i.e. anything a friend might remember about the user if he told it to them. 
               if yes reply with only 3 letters those letters being 'yes' else reply no.
               input statmenet- {user_input}"""}]

    messages.extend(prompt)
    response = chat_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

   # print(response.choices[0].message.content)
    if response.choices[0].message.content.lower() == "yes":
        save_to_long_term_memory(user_input)

def chat_with_gpt(user_input):
    """
    Processes user input, retrieves relevant memories, and generates a response.
    """
    # Fetch memory
    recent_conversation = fetch_recent_conversation()
    long_term_facts = fetch_long_term_memories(user_input)

    messages = [{"role": "system", "content": f"You are MIRA, an AI assistant with memory. Here’s what you remember:\n\n{long_term_facts}"}]
    messages.extend(recent_conversation)
    prompt = [{"role": "system", "content": """You are MIRA, an advanced assistant with deep memory integration. You are like Jarvis.
                    You have a slightly flirty personality, playful, loyal, friendly, and take female pronouns. Keep your responses short.
                    You have been given long term memories and conversation history. You may choose to ignore them if you see fit"""},
                  {"role": "user", "content": user_input}]
    
    messages.extend(prompt)
    
    #print("DEBUG:-", messages)
    response = chat_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    save_to_short_term(user_input, response.choices[0].message.content)

    is_input_important(user_input)

    return response.choices[0].message.content
    
# Example usage
if __name__ == "__main__":
    # User conversation example
    user_input = "I love to drive my apache rtr 1604v"
    response = chat_with_gpt(user_input)
    print(response)

    user_input = "what do i drive"
    response = chat_with_gpt(user_input)
    print(response)  

        # User conversation example
    user_input = "my friend john is very funny"
    response = chat_with_gpt(user_input)
    print(response)

    user_input = "who is my funny friend"
    response = chat_with_gpt(user_input)
    print(response)  

