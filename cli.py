from openai import OpenAI
import json
import os
import pyperclip
from typing import List, Dict

# To use this without environment variables follow these steps:
# Uncomment this (replace YOUR_API_KEY_HERE with your actual API key):
# api_key = "YOUR_API_KEY_HERE"

# Uncomment this:
# client = OpenAI(api_key=api_key)

# Place a # before this to comment it out:
client = OpenAI()

class ChatSession:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.messages = []
        self.last_response = ""

    def reset_chat(self):
        self.messages = []
        self.last_response = ""
        print("\033[92mConversation has been reset.\033[0m")

    def set_model(self, model_name: str):
        available_models = self.get_available_models()
        if model_name in available_models:
            self.model = model_name
            print(f"Model set to {model_name}")
        else:
            print(f"\033[91mError: Model '{model_name}' not found. Please use '?models' to see the list of available models.\033[0m")

    def get_available_models(self) -> List[str]:
        try:
            models = client.models.list()
            return [model.id for model in models.data if 'gpt' in model.id]
        except Exception as e:
            print(f"\033[91mAn error occurred while fetching models: {e}\033[0m")
            return []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def save_chat(self, filename: str = None):
        if filename is None:
            filename = str(self.generate_filename())
        filename += '.ai'
        with open(filename, 'w') as f:
            json.dump({"model": self.model, "messages": self.messages}, f)
        print(f"Chat saved to {filename}")

    def load_chat(self, filename: str):
        if not filename.endswith('.ai'):
            filename += '.ai'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.model = data["model"]
                self.messages = data["messages"]
                print("\033[93mChat Successfully Loaded:\033[0m")
            for message in self.messages:
                role = message["role"]
                content = message["content"]
                if role == "user":
                    print(f"\033[96m> {content}\033[0m")
                else:
                    print(f"\033[91m{role.capitalize()}: {content}\033[0m")
        else:
            print(f"\033[91mError: File '{filename}' not found.\033[0m")

    def delete_chat(self, filename: str):
        if not filename.endswith('.ai'):
            filename += '.ai'
        if os.path.exists(filename):
            os.remove(filename)
            print(f"\033[92mChat '{filename}' deleted successfully.\033[0m")
        else:
            print(f"\033[91mError: File '{filename}' not found.\033[0m")

    def stream_response(self):
        try:
            stream = client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
            assistant_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    assistant_response += chunk.choices[0].delta.content
                    print(f"\033[91m{chunk.choices[0].delta.content}\033[0m", end="")
            self.last_response = assistant_response
            self.add_message("assistant", assistant_response)
            print()
        except Exception as e:
            print(f"\033[92m An error occurred: {e}\033[0m")

    def generate_filename(self) -> str:
        self.add_message("system", "Generate a short one-word, maybe two, conversation unique filename for a chat conversation. Do not use quotes. Do not use a timestamp")
        response = client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        filename = response.choices[0].message.content
        return filename

    def regenerate_response(self):
        if self.messages:
            if self.messages[-1]["role"] == "assistant":
                self.messages.pop()
            self.stream_response()
        else:
            print("\033[91mNo previous conversation to regenerate.\033[0m")

    def copy_last_response(self, count: int = 1):
        if self.messages:
            recent_messages = self.messages[-count:]
            copied_text = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
            pyperclip.copy(copied_text)
            print(f"\033[92mCopied the last {count} message(s) to clipboard!\033[0m")
        else:
            print("\033[91mNo messages to copy.\033[0m")

    def copy_all(self):
        if self.messages:
            all_content = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in self.messages])
            pyperclip.copy(all_content)
            print("\033[92mAll conversation copied to clipboard!\033[0m")
        else:
            print("\033[91mNo conversation to copy.\033[0m")

    def list_saved_conversations(self):
        files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.ai')]
        if files:
            print("\033[92mSaved conversations:\033[0m")
            for file in files:
                print(f"\033[96m{file}\033[0m")
        else:
            print(f"\033[91mNo saved conversations found.\033[0m")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_help(self):
        print(f"\033[93mCommands: \033[0m")
        print(f"\033[93m----- \033[0m")
        print(f"\033[92m?model <model_name> | to set the model \033[0m")
        print(f"\033[92m?save <filename> | to save the chat with a .ai extension \033[0m")
        print(f"\033[92m?load <filename> | to load a chat \033[0m")
        print(f"\033[92m?delete <filename> | to delete a chat \033[0m")
        print(f"\033[92m?copy [number] | to copy the assistant's last response or the last number of messages \033[0m")
        print(f"\033[92m?reset | to reset the conversation \033[0m")
        print(f"\033[92m?regen | to regenerate the last response \033[0m")
        print(f"\033[92m?list | to list all saved conversations with a .ai extension \033[0m")
        print(f"\033[92m?models | to list all available models \033[0m")
        print(f"\033[92m?clear | to clear the screen \033[0m")
        print(f"\033[92m?quit | to quit the program \033[0m")
        print(f"\033[92m?help | to show this help message \033[0m")
        print(f"\033[93m----- \033[0m")
        print("\033[93mType your message to send to the model\033[0m")

    def list_models(self):
        try:
            models = client.models.list()
            print("\033[92mAvailable text models:\033[0m")
            for model in models.data:
                if 'gpt' in model.id:
                    print(model.id)
        except Exception as e:
            print(f"\033[91mAn error occurred while fetching models: {e}\033[0m")

def main():
    session = ChatSession()
    session.show_help()

    while True:
        command = input("> ")
        cmd_parts = command.split(" ")
        cmd = cmd_parts[0].lower()

        if cmd in ["?model"]:
            model_name = cmd_parts[1]
            session.set_model(model_name)
        elif cmd in ["?save"]:
            filename = cmd_parts[1] if len(cmd_parts) > 1 else None
            session.save_chat(filename)
        elif cmd in ["?load"]:
            filename = cmd_parts[1]
            session.load_chat(filename)
        elif cmd in ["?delete"]:
            filename = cmd_parts[1]
            session.delete_chat(filename)
        elif cmd in ["?copy", "?cpall", "?copyall", "?cp"]:
            if cmd == "?copyall" or cmd == "?cpall":
                session.copy_all()
            else:
                if len(cmd_parts) == 1:
                    session.copy_last_response()
                else:
                    try:
                        count = int(cmd_parts[1])
                        session.copy_last_response(count)
                    except ValueError:
                        print("\033[91mInvalid number specified for copying messages.\033[0m")
        elif cmd in ["?reset", "?rst"]:
            session.reset_chat()
        elif cmd in ["?regen", "?rg"]:
            session.regenerate_response()
        elif cmd in ["?list", "?lst"]:
            session.list_saved_conversations()
        elif cmd in ["?models", "?mdl"]:
            session.list_models()
        elif cmd in ["?clear", "?clr"]:
            session.clear_screen()
        elif cmd in ["?help", "?h"]:
            session.show_help()
        elif cmd in ["?quit", "?exit", "?q"]:
            print("\033[92mQuitting the program...\033[0m")
            break
        elif cmd.startswith("?"):
            print(f"\033[91mError: Invalid command '{command}'\033[0m")
        else:
            session.add_message("user", command)
            session.stream_response()

if __name__ == "__main__":
    main()
