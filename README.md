# Lightweight Free LLM API
A lightweight free virtual machine on google colab 
Tunneled using Ngrok to any user with url
Hosting an ollama LLM manager
With weights of your choosing (currently Qwen 2.5 (14B))

Instance only needs few minutes of setup 
From any device with internet
Completely offloaded,
And fully customisable memory and context.
(currently 4096 tokens or 50 messages if message is 50 words average).

## Pt1: How to setup server:

### Prerequisites
Have a google account

### 1.1 Grab the token

Ngrok is our tunnel to secure connection with google colab's virtual machine.
You will need to make an account at https://ngrok.com/ 
You can just sign in with your google account. 
You DONT need to do any installation,
Just go to "Your Authtoken" tab and save your token.


### 1.2 Setup Google colab

Google colab holds virtual machines that house powerful GPU's for free.
We need the VRAM to power the number of weights in a LLM. 
Go to the website with your google account.
https://colab.research.google.com/ 
And start a new notebook.
Go Runtime > change runtime type > Hardware accelerator = T4GPU. 
Go secrets > tick notebook access, put in NGROK_TOKEN, and your token you saved.
Make sure to save your notebook.

### 1.3 Setup LLM server

In Google Colab code, ctrl+c the code
Place it into a single code block in the colab notebook.
Press run all.
This will create a tunnel running in the background .
It will last a few hours or until you close it .
The output will be an API URL:
This is our entry point to local instances.
Paste it into "server_url.txt"


## Pt2: How to call and use LLM locally

### Prerequisites
Have vscode installed. 
With python installed.

### 2.1 Setup Python environment

In our local application, we will be using python. 
Open the terminal tab in vscode.
Make a virtual environment.
This is done via:

```python3 -m venv .venv```

You can then activate any time via:

```source .venv/bin/activate```

For macOS/linux.
If your environment doesnt work for this, 
a browser search can provide the two simple lines needed.
Then we will install the library needed: 

``` pip install requests```

### 2.2 Try the study app executable

sovereign_client.py represents the general class and tools that the AI server gets run with.
Following, we use an executable that imports the class such as study_app.py, which is our simplest example.
Run it using:

```python3 ./Sovereign_AI/study_app.py```

Afterwards, simply enjoy and follow the guidance!

## Pt3: Learn to build yourself

Recall that the model weights is from Qwen 2.5 (14B).
This is a quantised model to fit the free google colab VRAM. 
The settings of this model and the application of its architecture from Ollama are done in the sovereign_client.py. 
This is the general class any executable calls. 
And assigns the model made in the server this classes attributes. 
Currently the features are:

50 maximum size of memory (25 turns), will forget earliest turn if surpass. 

Able to compress memory to continue chat more effectively (via compress_memory)

Able to set general system prompt and completely reset memory (via set_persona)

Able to reset memory but not change system prompt (via clear_memory)

Able to undo last turn (via forget_last)

Able to vary temperature (via chat)

chat is also the method that does the actual chatting. 


An example of its implementation in its simplest form is shown in study_app.py, 
Which is a simple terminal input form of the class. 







