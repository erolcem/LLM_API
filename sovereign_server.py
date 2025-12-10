# ==============================================================================
#                      THE SOVEREIGN SERVER (GOOGLE COLAB)
# ==============================================================================
# INSTRUCTIONS:
# 1. Menu -> Runtime -> Change Runtime Type -> T4 GPU
# 2. Add your Ngrok Token to the "Secrets" (Key icon on left) named 'NGROK_TOKEN'
#    (Or just paste it when prompted).
# 3. Run this cell.
# ==============================================================================

import os
import subprocess
import time
import sys

# --- 1. PROVISIONING & INSTALLATION ---
print("⚙️ [1/5] Installing Dependencies (Ollama & Ngrok)...")
if subprocess.run("pip install pyngrok", shell=True).returncode != 0:
    print("❌ Failed to install pyngrok")
    sys.exit(1)

# Install Ollama (Silently)
subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# --- 2. AUTHENTICATION ---
print("🔑 [2/5] Authenticating Ngrok...")
from google.colab import userdata
from pyngrok import ngrok

try:
    token = userdata.get('NGROK_TOKEN')
    print("   -> Token retrieved from Secrets Manager.")
except:
    token = input("   -> Secrets not found. Paste Ngrok Token here: ")

ngrok.set_auth_token(token)

# --- 3. CONFIGURATION (CORS & PORTS) ---
print("🛡️ [3/5] Configuring Network Permissions...")
# Kill any existing Ollama processes to prevent conflicts
subprocess.run("pkill ollama", shell=True)
time.sleep(2)

# Set Environment Variables to allow external connections (Fixes 403 Forbidden)
os.environ["OLLAMA_ORIGINS"] = "*"
os.environ["OLLAMA_HOST"] = "0.0.0.0"

# --- 4. STARTING THE ENGINE ---
print("🚀 [4/5] Spinning up Ollama Engine (Background)...")
process = subprocess.Popen(
    ["ollama", "serve"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(5) # Allow warmup

# Open the Tunnel
try:
    # Kill old tunnels
    ngrok.kill()
    tunnel = ngrok.connect(11434)
    public_url = tunnel.public_url
    print(f"   -> Tunnel Established.")
except Exception as e:
    print(f"❌ Tunnel Error: {e}")
    sys.exit(1)

# --- 5. LOADING THE BRAIN ---
MODEL_NAME = "qwen2.5:14b"
print(f"⬇️ [5/5] Downloading Model: {MODEL_NAME} (This takes ~2-5 mins)...")
# We pull the model. This is the blocking step.
subprocess.run(f"ollama pull {MODEL_NAME}", shell=True)

print("\n" + "="*60)
print(f"✅ SYSTEM ONLINE")
print(f"🔗 API URL: {public_url}")
print("="*60)
print("⚠️ COPY THE URL ABOVE INTO YOUR LOCAL CLIENT SCRIPT ⚠️")