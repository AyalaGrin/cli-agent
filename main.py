import os
import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv
import gradio as gr
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# הפונקציה מקבלת כעת גם את ההודעה וגם את היסטוריית השיחה
def generate_cli_command(message, history):
    if not message.strip():
        return "אנא הזן הוראה בשפה טבעית."
    
    system_instruction = (
        "You are a specialized assistant for converting requests into Command Line Interface (CLI) commands.\n"
        "Your sole function is to translate natural language requests into precise terminal commands that can be executed directly.\n\n"
        "Strict Domain Rules and Validation:\n"
        "1. Valid Input: Only requests that directly describe a system operation, file management task, or network task are considered valid.\n"
        "2. Invalid Input:\n"
        "Any query requesting general information, weather data, identity verification, or conversational interaction is strictly considered invalid.\n"
        "Any query requiring the use of content unrelated to system operations—such as website links, general web pages, or entertainment, leisure, or news content—is strictly considered invalid.\n"
        "Prohibited Commands:\n"
        "Any query that would result in a high-risk command requiring user confirmation before execution is strictly forbidden (e.g., `del`, `rm -rf`, `shutdown`, `format`).\n"
        "3. Output Format:\n"
        "For valid input: Return only the precise, raw shell command, without any Markdown formatting or backticks. For non-standard input, return exactly the following text: 'Error: The input is not related to a terminal command.'\n\n"
        "Examples:\n"
        "User: Create a new folder named project\n"
        "Output: mkdir project\n"
        "User: What is your name?\n"
        "Output: Error: The input is not related to a terminal command.\n"
        "User: What is the weather like in Jerusalem?\n"
        "Output: Error: The input is not related to a terminal command."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message,
            config={'system_instruction': system_instruction}
        )
        
        return response.text.strip()

    except Exception as e:
        return f"שגיאה בהתחברות ל-Gemini: {str(e)}"

# שימוש ב-gr.ChatInterface ליצירת ממשק בצורת צ'אט
demo = gr.ChatInterface(
    fn=generate_cli_command,
    title="CLI Agent - Natural Language to Terminal",
    textbox=gr.Textbox(placeholder="הזיני הוראה בשפה טבעית...", container=False, scale=7)
)

if __name__ == "__main__":
    demo.launch()