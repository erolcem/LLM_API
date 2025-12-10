# Lightweight Free LLM API
A lightweight free virtual machine on google colab 
Tunneled using Ngrok to any user with url
Hosting an ollama LLM manager
With weights of your choosing (currently Qwen 2.5 (14B))

Instance only needs few minutes of setup 
From any device with internet
Completely offloaded,
And fully customisable memory and context.

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
Go Runtime > change runtime type > Hardware accelerator = T4GPU
Go secrets > tick notebook access, put in NGROK_TOKEN, and your token you saved.
Make sure to save your notebook.

### 1.3 Setup LLM server

In Google Colab code, ctrl+c the code
Place it into a single code block in the colab notebook.
Press run all
This will create a tunnel running in the background 
It will last a few hours or until you close it 
The output will be an API URL:
Save this as your access point to use locally.


## Pt2: How to call use LLM locally

