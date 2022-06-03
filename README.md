# Virtual Assistant
Virtual Assistant is a voice commanding assistant service. It can recognize human speech, talk to user and execute
basic commands. \
Tested and working on Windows 10.

## Installation
Clone the repository
```
git clone https://github.com/Kowalski1024/Virtual-Assistant.git
```
Create virtual environment, for example
```
python -m venv venv
```
Activate virtual environment
```
.\venv\Scripts\activate
```
Install application dependencies
```
pip install -r requirements.txt
```
Install pyaudio
```
pip install pipwin
pipwin install pyaudio
```
or download and install from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) \
Run the assistant
```
python .\run.py
```

[comment]: <> (## How to use)

[comment]: <> (Assistant will activate when the user presses a keyboard shortcut `win+w`, )

[comment]: <> (there will be a sound effect indicating that the assistant is waiting for speech input.)