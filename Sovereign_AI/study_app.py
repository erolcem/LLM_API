import os
import sys
# Import the class we just created
from sovereign_client import SovereignClient

# =========================================================
# ⚠️ CONFIGURATION: Update server_url.txt with your ngrok URL
# =========================================================
def load_server_url():
    """Load server URL from server_url.txt file"""
    try:
        with open('server_url.txt', 'r') as f:
            url = f.read().strip()
            if url:
                return url
            else:
                print("❌ ERROR: server_url.txt is empty")
                sys.exit(1)
    except FileNotFoundError:
        print("❌ ERROR: server_url.txt not found. Please create it with your ngrok URL.")
        sys.exit(1)

SERVER_URL = load_server_url()
# =========================================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("🎓 SOVEREIGN STUDY COMPANION (v2.0)")
    print("-----------------------------------")
    print("Type '/undo' to fix mistakes.")
    print("Type '/compress' to save memory.")
    print("Type '/quit' to exit.")
    print("-----------------------------------")
    
    # 1. Initialize
    bot = SovereignClient(SERVER_URL)
    
    # 2. Connection Check
    print("📡 Connecting to Brain...", end="\r")
    response = bot.chat("Are you online? Reply with 'Ready'.")
    if "Error" in response:
        print(f"\n{response}")
        print("Check if Google Colab is running and the URL is updated.")
        sys.exit()
    print("✅ System Online & Ready.  \n")

    # 3. Mode Selection
    while True:
        print("\nSELECT MODE:")
        print("1. Socratic Tutor (Learn by answering)")
        print("2. Exam Simulator (Test your knowledge)")
        print("3. Free Chat (Just talk)")
        print("Q. Quit")
        
        choice = input("Choice: ").upper()
        
        if choice == "Q":
            break
            
        topic = ""
        if choice in ["1", "2"]:
            topic = input("Enter Topic (e.g., 'Op-Amps', 'Calculus'): ")

        # --- POWER CUSTOMIZATION ---
        if choice == "1":
            bot.set_persona(
                f"You are a Socratic Tutor teaching {topic}. "
                "Never explain the concept directly. "
                "Ask one simple question at a time to lead the user to the answer. "
                "If they are wrong, give a hint."
            )
            print(f"\n--- SOCRATIC SESSION: {topic} ---")
            print(f"AI: Let's begin. What do you already know about {topic}?")
            
        elif choice == "2":
            bot.set_persona(
                f"You are a strict Examiner for {topic}. "
                "Ask a hard technical question. Wait for the answer. "
                "Then grade it 0-10, explain the correction, and ask the next question."
            )
            print(f"\n--- EXAM SESSION: {topic} ---")
            print(f"AI: I am generating your first question on {topic}...")
            # Trigger the first question
            print(bot.chat(f"Ask me the first question about {topic}."))

        elif choice == "3":
            bot.set_persona("You are a helpful, sarcastic engineering assistant.")
            print("\n--- FREE CHAT ---")

        # 4. The Conversation Loop (With Magic Commands)
        while True:
            try:
                user_input = input("\nYou: ")
                
                # --- MAGIC COMMANDS ---
                if user_input.lower() in ['/quit', '/exit']:
                    break
                
                elif user_input.lower() == '/undo':
                    bot.forget_last()
                    continue # Skip sending this to AI
                
                elif user_input.lower() == '/compress':
                    bot.compress_memory()
                    continue
                
                elif user_input.lower() == '/wipe':
                    bot.clear_memory()
                    print("Memory cleared.")
                    continue
                
                # Normal Message Handling
                print("Thinking...", end="\r")
                temp = 0.2 if choice == "2" else 0.7
                reply = bot.chat(user_input, temperature=temp)
                
                print(" " * 20, end="\r")
                print(f"AI: {reply}")
                
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()