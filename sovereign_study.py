import requests
import json
import sys
import os

# --- CONFIGURATION ---
# ⚠️ UPDATE THIS URL EVERY TIME YOU RESTART COLAB ⚠️
SERVER_URL = "https://oldfangled-uniambic-aryanna.ngrok-free.dev"  

class SovereignClient:
    """The Client Logic (The Body)"""
    def __init__(self, api_url, model="qwen2.5:14b", system_prompt="You are a helpful assistant."):
        self.api_url = api_url.rstrip('/') + "/api/chat"
        self.model = model
        self.headers = {"ngrok-skip-browser-warning": "true", "Content-Type": "application/json"}
        self.system_prompt = {"role": "system", "content": system_prompt}
        self.chat_history = [] 
        self.max_history = 20 

    def chat(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})
        
        # Sliding Window Memory
        if len(self.chat_history) > self.max_history:
            self.chat_history.pop(0)
            self.chat_history.pop(0)

        full_context = [self.system_prompt] + self.chat_history
        payload = {
            "model": self.model, 
            "messages": full_context, 
            "stream": False,
            "options": {"temperature": 0.7}
        }

        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=120)
            response.raise_for_status()
            ai_msg = response.json()['message']['content']
            self.chat_history.append({"role": "assistant", "content": ai_msg})
            return ai_msg
        except requests.exceptions.ConnectionError:
            return "❌ ERROR: Cannot connect to Colab. Is the server running and URL correct?"
        except Exception as e:
            return f"❌ ERROR: {e}"

def clear_screen():
    # Clears the terminal for a nice UI feel
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("==========================================")
    print("      SOVEREIGN STUDY AID (LOCAL)         ")
    print("      Connected to: Qwen 14B (Cloud)      ")
    print("==========================================")

    # 1. Connection Test
    print("📡 Testing connection to Colab...", end="\r")
    try:
        # We send a dummy request to check if the brain is awake
        requests.get(SERVER_URL, timeout=5) 
        print("✅ Connection Established!          \n")
    except:
        print("❌ CONNECTION FAILED.             ")
        print("Check your NGROK URL in the script.")
        return

    # 2. Mode Selection
    print("1. Socratic Tutor")
    print("2. Exam Simulator")
    mode = input("\nSelect Mode (1/2): ")
    topic = input("Enter Topic: ")
    
    system_prompt = ""
    if mode == "1":
        system_prompt = f"You are a Socratic Tutor on {topic}. Ask questions to guide the user. Do not give answers."
        print(f"\n👨‍🏫 SOCRATIC MODE: {topic}")
    else:
        system_prompt = f"You are a strict Examiner on {topic}. Ask hard questions and grade the answers."
        print(f"\n📝 EXAM MODE: {topic}")

    bot = SovereignClient(SERVER_URL, system_prompt=system_prompt)
    
    # 3. Initial Trigger
    initial = bot.chat("Begin the session.")
    print(f"\nAI: {initial}")

    # 4. Chat Loop
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['quit', 'exit']:
                break
            
            print("Thinking...", end="\r")
            response = bot.chat(user_input)
            
            # Overwrite "Thinking..." with the answer
            print(" " * 20, end="\r") 
            print(f"AI: {response}")
            
        except KeyboardInterrupt:
            print("\n\nSession Interrupted.")
            break

if __name__ == "__main__":
    main()