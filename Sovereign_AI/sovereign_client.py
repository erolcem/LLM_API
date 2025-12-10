### SOVEREIGN CLIENT CLASS
# This is the universal client that can connect to the AI server hosted on Colab.
# It manages the conversation history, personas, and handles communication.
# we have init --> this initiates model for use (with a system prompt)
# we have reset_history --> ai forgets all chats 
# we have chat --> allows for LLM use (with temperature control
# Has reasonable memory garbage collection to avoid overloading context window, yet maintain long conversations.
# we have set_persona --> allows changing of system prompt
# we have clear_memory --> wipes all chat history but keeps persona
# we have forget_last --> removes last user + ai message
# we have compress_memory --> advanced feature to summarize chat history into a single message to save space
# This client can be used in any local Python environment to connect to the Colab-hosted AI.

import requests
import json

class SovereignClient:
    """
    The Universal Client for your Cloud AI.
    Handles connection, memory management, and personas.
    """
    def __init__(self, api_url, model="qwen2.5:14b", system_prompt="You are a helpful assistant."):
        # Clean the URL (User often pastes with or without slash)
        self.api_url = api_url.rstrip('/') + "/api/chat"
        self.model = model
        
        # Headers to bypass Ngrok's "Phishing Warning" page
        self.headers = {
            "ngrok-skip-browser-warning": "true",
            "Content-Type": "application/json"
        }
        
        # Memory Initialization
        self.system_prompt_content = system_prompt
        self.history = [] 
        
        # INCREASED LIMIT: 50 turns (User + AI) is safe for Qwen 14B on T4 GPU
        self.max_history = 50 
        
        # Set initial system prompt
        self._reset_history()

    def _reset_history(self):
        """Internal helper to rebuild memory with current system prompt."""
        self.history = [{"role": "system", "content": self.system_prompt_content}]

    def chat(self, user_input, temperature=0.7):
        """
        Send message to server and get response.
        :param temperature: 0.1 = Robotic/Precise, 0.9 = Creative/Random
        """
        # 1. Update Local Memory
        self.history.append({"role": "user", "content": user_input})
        
        # 2. Sliding Window (Garbage Collection)
        # If history exceeds limit, remove oldest messages (but KEEP index 0 which is System Prompt)
        # We check > max_history + 1 because history[0] is the system prompt
        if len(self.history) > self.max_history + 1:
            self.history.pop(1) # Remove oldest User message
            self.history.pop(1) # Remove oldest AI message

        # 3. Build Payload
        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": False,
            "options": {"temperature": temperature}
        }

        # 4. Transmit
        try:
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=120)
            response.raise_for_status()
            
            # 5. Process Response
            data = response.json()
            ai_msg = data['message']['content']
            
            # Add AI response to memory
            self.history.append({"role": "assistant", "content": ai_msg})
            return ai_msg

        except requests.exceptions.ConnectionError:
            return "❌ NETWORK ERROR: Cannot reach Colab. Is the URL correct?"
        except Exception as e:
            return f"❌ SYSTEM ERROR: {e}"

    def set_persona(self, new_prompt):
        """Clears memory and applies a new personality."""
        self.system_prompt_content = new_prompt
        self._reset_history()
        print(f"\n🔄 System Persona Updated.")

    def clear_memory(self):
        """Wipes conversation but keeps current persona."""
        self._reset_history()
        print("🧹 Memory Wiped.")

    def forget_last(self):
        """Undoes the last turn (Removes 1 User msg + 1 AI msg)."""
        if len(self.history) > 1:
            self.history.pop() # Pop AI response
            self.history.pop() # Pop User prompt
            print("Action Undone. Memory rolled back.")
        else:
            print("Nothing to forget.")

    def compress_memory(self):
        """
        ADVANCED: Asks the AI to summarize the chat so far, 
        then wipes history and replaces it with the summary.
        Use this if you want to talk for hours.
        """
        print("🗜️ Compressing Memory...", end="\r")
        
        # Create a temporary one-off request
        summary_request = self.history + [{"role": "user", "content": "Summarize our conversation so far in one detailed paragraph. Preserve key facts and code snippets."}]
        
        payload = {
            "model": self.model,
            "messages": summary_request,
            "stream": False
        }
        
        try:
            # We don't use self.chat() because we don't want this in the history
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=120)
            summary_text = response.json()['message']['content']
            
            # Rewrite History: System Prompt + Summary
            self.history = [
                {"role": "system", "content": self.system_prompt_content},
                {"role": "assistant", "content": f"MEMORY CONTEXT: {summary_text}"}
            ]
            print("✅ Memory Compressed. Space Reclaimed.")
            return summary_text
            
        except Exception as e:
            print(f"❌ Compression Failed: {e}")