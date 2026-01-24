# ==============================================================================
#                      THE SOVEREIGN SERVER (GOOGLE COLAB)
# ==============================================================================
# TRY THIS ONE IF THE soverign_server.py FAILS TO INSTALL OLLAMA
# ==============================================================================

import os
import subprocess
import time
import sys

# --- 1. PROVISIONING & INSTALLATION ---
print("⚙️ [1/5] Installing Dependencies (Ollama & Ngrok)...")

# Install pyngrok
pyngrok_install_cmd = "pip install pyngrok"
print(f"   -> Running: {pyngrok_install_cmd}")
if subprocess.run(pyngrok_install_cmd, shell=True).returncode != 0:
    print("❌ Failed to install pyngrok")
    sys.exit(1)
else:
    print("   -> pyngrok installed.")

# Install zstd, a dependency for Ollama
print("   -> Installing zstd...")
if subprocess.run("sudo apt-get update && sudo apt-get install -y zstd", shell=True).returncode != 0:
    print("❌ Failed to install zstd")
    sys.exit(1)
else:
    print("   -> zstd installed.")

# Install Ollama (Make it verbose to check for errors)
print("   -> Installing Ollama...")
# Use `sh -s -- -y` to non-interactively install, agreeing to prompts.
# This typically installs to /usr/local/bin
install_ollama_cmd = "curl -fsSL https://ollama.com/install.sh | sh -s -- -y"
install_result = subprocess.run(install_ollama_cmd, shell=True, capture_output=True, text=True)

if install_result.returncode != 0:
    print("❌ Failed to install Ollama.")
    print("STDOUT:", install_result.stdout)
    print("STDERR:", install_result.stderr)
    sys.exit(1)
else:
    print("   -> Ollama installation successful.")
    # print("STDOUT:", install_result.stdout) # Uncomment for more verbose output if needed
    # print("STDERR:", install_result.stderr)

# Determine the full path to the ollama executable
ollama_executable = "/usr/local/bin/ollama"
# Verify if it exists, if not, try to find it (though /usr/local/bin is standard)
if not os.path.exists(ollama_executable):
    print(f"⚠️ Warning: Ollama not found at expected path {ollama_executable}. Attempting to locate.")
    try:
        # Use 'which' to find the executable in the PATH
        which_result = subprocess.run("which ollama", shell=True, capture_output=True, text=True, check=True)
        ollama_executable = which_result.stdout.strip()
        print(f"   -> Found Ollama at: {ollama_executable}")
    except subprocess.CalledProcessError:
        print("❌ Could not locate Ollama executable after installation. Please check the installation logs.")
        sys.exit(1)

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
# Use the determined ollama_executable for pkill
subprocess.run(f"pkill -f {ollama_executable}", shell=True)
time.sleep(2)

# Set Environment Variables to allow external connections (Fixes 403 Forbidden)
os.environ["OLLAMA_ORIGINS"] = "*"
os.environ["OLLAMA_HOST"] = "0.0.0.0"

# --- 4. STARTING THE ENGINE ---
print("🚀 [4/5] Spinning up Ollama Engine (Background)...")
process = subprocess.Popen(
    [ollama_executable, "serve"],
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
# Use the determined ollama_executable for ollama pull
subprocess.run(f"{ollama_executable} pull {MODEL_NAME}", shell=True)

print("\n" + "="*60)
print(f"✅ SYSTEM ONLINE")
print(f"🔗 API URL: {public_url}")
print("="*60)
print("⚠️ COPY THE URL ABOVE INTO YOUR LOCAL CLIENT SCRIPT ⚠️")