# Virtual Assistant

Virtual Assistant is a voice commanding assistant service. It can recognize human speech, talk to user and execute basic
commands. \
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

or download and install from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio). \
Run the assistant

```
python .\run.py
```

### Run tests

```
python -m unittest discover -s .\assistant\tests\
```

## How to use assistant

Assistant will activate when the user presses a keyboard shortcut `win+w`, there will be a sound effect indicating that
the assistant is waiting for speech input.

### Assistant's skills

Below is a list of voice commands that activate a specific assistant skill. All skills can be found in the
[registry.py](assistant_archive/skills/registry.py) file, and more information on how they work can be found in the 
[collection dictionary](assistant_archive/skills/collection).

#### Assistant skills
1. `voice` - changes the assistant's replay mode to voice
2. `text` - changes the assistant's replay mode to text

#### Browser skills
1. `wikipedia` - searches given keyword on Wikipedia
2. `open` - opens a web page in the browser
3. `search` - opens google.com with search results for given keyword
4. `synonyms` - displays synonyms for the word the user specified

#### Weather skills
1. `weather` - gets weather for given city

#### Reminder skills
1. `remind` - creates a simple reminder for the given time interval (seconds or minutes or hours)

#### Calendar skills
1. `show calendar` - gets events from Outlook Calendar in given range
2. `add event` - creates an event in Outlook calendar

#### Email skills
1. `send email` - creates an email based on user input, sends it or saves as draft or cancels it
