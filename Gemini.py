import google.generativeai as genai
import pyttsx3

genai.configure(api_key="Your API KEY")

# Create the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.5,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="",
)
# [{role,parts:[],},{role,parts:[],}]
chat_session = model.start_chat(history=[])


import json


def write_conversation_to_json(filepath, user_input, model_output):
    """Writes a user input and model output to a JSON file.

    Args:
        filepath: The path to the JSON file.
        user_input: The text of the user's input.
        model_output: The text of the model's output.
    """

    new_data = [
        {"role": "user", "parts": [user_input]},
        {"role": "model", "parts": [model_output]},
    ]

    try:
        with open(filepath, "r+") as f:
            if f.read(1):  # Check if file is not empty
                f.seek(0)
                existing_data = json.load(f)
            else:
                existing_data = []

            existing_data.extend(new_data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)

    except FileNotFoundError:
        with open(filepath, "w") as f:
            json.dump(new_data, f, indent=4)


def save_to_markdown(content):
    with open("response.md", "a") as f:  # Open in append mode
        f.write(content + "\n\n")  # Add two new lines for separation


# Function to generate content and save history
def chat_with_gemini(user_input):
    # Generate response from the model
    response = chat_session.send_message(user_input)
    response_text = response.text

    # Prepare the content to save
    conversation_entry = f"**You  :** {user_input}\n\n**Gemini:** {response_text}\n\n"

    # Save the conversation entry to the markdown file
    save_to_markdown(conversation_entry)

    filepath = "response.json"
    write_conversation_to_json(filepath, user_input, response_text)

    # this is just for only voice
    content = response_text.split("*")
    my_string = " ".join(content)
    engine = pyttsx3.init()
    engine.setProperty("rate", 140)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(my_string)
    engine.runAndWait()

    # Print the response
    print(response_text)


# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        chat_with_gemini(user_input)
