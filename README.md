# twitch_chat_analyzer
![license](https://img.shields.io/badge/license-MIT%20License-blue.svg)

analyze when viewers enter certain words at a lot
you can find time of a specific chat

implement: python 3.7 
module
``` python
Default 
  json
  tKinter
require install
  requests
  numpy
  matplotlib
  pyinstaller
  QTPY5
```

## how to use

1. download zip or git clone this repository

2-1. run app.py

2-2. make exe file & run dist/app.exe

``` terminal
pyinstaller --onefile --noconsole --icon=twitch.ico app.py
```

![first](https://github.com/asdfghjkkl11/twitch_chat_analyzer/blob/master/dist/1.PNG)

3. input videoID & clientID, click load button. 
  then load chat log of video.
  
![second](https://github.com/asdfghjkkl11/twitch_chat_analyzer/blob/master/dist/2.PNG)

4. input words you want to find (words are separated by space)
  then show frequency graph of that words 
