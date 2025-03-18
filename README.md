# M.I.R.A. - My Intelligent Reliable Assistant

Welcome to M.I.R.A., your personal AI assistant designed to be as close to J.A.R.V.I.S. as reality allows (for now). Whether you need help managing tasks, playing music, launching apps, or just having a solid conversation, M.I.R.A. has you covered. 

## Why M.I.R.A.?
Because life is better with a smart assistant who remembers what matters, processes your requests intelligently, and controls your digital world like a pro. This is not just another chatbot—it has memory, music control, and the ability to run your applications on command. The goal? A true AI companion, growing with every update.

## Setup - Get M.I.R.A. Running
To unleash M.I.R.A.'s full potential, you’ll need:
- **MongoDB** - To store memory and data
- **ChatGPT API** - For intelligent conversation
- **FastAPI** - To handle backend operations
- **Spotify API** - For seamless music control
- **PyQt** - For the slick graphical interface

### Steps to Get Started:
1. Clone this repository into a folder of your choice.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Set up a MongoDB database named `data` in the same directory.
4. Update the `.env` file with your API keys (ChatGPT, Spotify, etc.).
5. Run `import_memories.py` once to load any initial long-term memories.
6. Launch M.I.R.A. by running `main.py`.

## How It Works
M.I.R.A. operates with a **PyQt frontend** and a **FastAPI backend** to handle requests smoothly. It processes:
- **User prompts** using ChatGPT
- **Conversations** with short-term and long-term memory
- **Spotify music control** (yes, it knows your vibe)
- **App launching** for anything installed on your machine

![alt text](<Screenshot 2025-02-23 232041.png>)

## What's Next?
This is just the beginning. The next iteration will focus on:
- **Speech-to-Text Integration** - So you can talk to M.I.R.A. hands-free
- **More Refined Spotify Management** - Think personalized playlists and smarter song control

M.I.R.A. is here to make your life easier. And let’s be honest, it’s just cool to have your own AI assistant. 

Contribute, improve, and help turn this into something even more powerful!

