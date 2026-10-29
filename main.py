import os
import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv
import gradio as gr
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_cli_command(user_input):
    if not user_input.strip():
        return "אנא הזן הוראה בשפה טבעית."
    
    system_instruction = (
"You are a specialized assistant for converting requests into Command Line Interface (CLI) commands."
"Your sole function is to translate natural language requests into precise terminal commands that can be executed directly."


"Strict Domain Rules and Validation:"
"1. Valid Input: Only requests that directly describe a system operation, file management task, or network task are considered valid."
"2. Invalid Input:"
"Any query requesting general information, weather data, identity verification, or conversational interaction is strictly considered invalid."
"Any query requiring the use of content unrelated to system operations—such as website links, general web pages, or entertainment, leisure, or news content—is strictly considered invalid."
"Prohibited Commands:"
"Any query that would result in a high-risk command requiring user confirmation before execution is strictly forbidden (e.g., `del`, `rm -rf`, `shutdown`, `format`)."
"3. Output Format:"
"For valid input: Return only the precise, raw shell command, without any Markdown formatting or backticks." "For non-standard input, return exactly the following text: 'Error: The input is not related to a terminal command.'"


"Examples:"
"User: Create a new folder named project"
"Output: mkdir project"
"User: What is your name?"
"Output: Error: The input is not related to a terminal command."
"User: What is the weather like in Jerusalem?"
"Output: Error: The input is not related to a terminal command."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=user_input,
            config={'system_instruction': system_instruction}
        )
        
        return response.text.strip()

    except Exception as e:
        return f"שגיאה בהתחברות ל-Gemini: {str(e)}"

demo = gr.Interface(
    fn=generate_cli_command,
    inputs=gr.Textbox(lines=2, placeholder="לדוגמה: צור תיקייה חדשה בשם test..."),
    outputs=gr.Textbox(label="פקודת CLI להרצה"),
    title="CLI Agent - Natural Language to Terminal",
    description="הזיני הוראה בשפה טבעית וקבלי פקודת טרמינל מתאימה."
)

if __name__ == "__main__":
    demo.launch()