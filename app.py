# -*- coding: utf-8 -*-
import requests
import json
from tkinter import *
from tkinter import messagebox
import tkinter.constants as Tkconstants
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

chat = []
time = []
user = []
new = None
canvas = None
ax = None


def doubleDigit(num):
    if num < 10:
        return '0' + str(num)
    else:
        return str(num)


def load():
    global chat
    global time
    global user
    nextCursor = ''
    params = {}
    video_id = text_V.get().strip()
    client_id = text_C.get().strip()
    if video_id == "":
        messagebox.showinfo('warnning', 'video_id is empty')
        return
    elif client_id == "":
        messagebox.showinfo('warnning', 'client_id is empty')
        return
    params['client_id'] = client_id
    text_A.delete(0, 'end')
    chat.clear()
    time.clear()
    user.clear()
    i = 0
    try:
        while True:
            if i == 0:
                URL = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'
                i += 1
            else:
                URL = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor='
                URL += nextCursor
            response = requests.get(URL, params=params)
            j = json.loads(response.text)
            for k in range(0, len(j["comments"])):
                timer = j["comments"][k]["content_offset_seconds"]
                timeMinute = int(timer / 60)
                if timeMinute >= 60:
                    timeHour = int(timeMinute / 60)
                    timeMinute %= 60
                else:
                    timeHour = int(timeMinute / 60)
                timeSec = int(timer % 60)
                time.append(doubleDigit(timeHour) + ':' + doubleDigit(timeMinute) + ':' + doubleDigit(timeSec))
                user.append(j["comments"][k]["commenter"]["display_name"])
                chat.append(j["comments"][k]["message"]["body"])
            if '_next' not in j:
                break
            nextCursor = j["_next"]

        for x in range(0, len(time)):
            alog = '[' + str(time[x]) + '] <' + str(user[x]) + '> ' + str(chat[x]) + "\n"
            text_A.insert(x, alog)
    except:
        messagebox.showinfo('warnning', 'video ID or client ID is wrong')
        return


def graph():
    def addScrollingFigure(figure, frame):
        global canvas, mplCanvas, interior, interior_id, cwid
        # set up a canvas with scrollbars
        canvas = Canvas(frame)
        canvas.grid(row=1, column=1, sticky=Tkconstants.NSEW)

        xScrollbar = Scrollbar(frame, orient=Tkconstants.HORIZONTAL)
        yScrollbar = Scrollbar(frame)

        xScrollbar.grid(row=2, column=1, sticky=Tkconstants.EW)
        yScrollbar.grid(row=1, column=2, sticky=Tkconstants.NS)

        canvas.config(xscrollcommand=xScrollbar.set)
        xScrollbar.config(command=canvas.xview)
        canvas.config(yscrollcommand=yScrollbar.set)
        yScrollbar.config(command=canvas.yview)

        # plug in the figure
        figAgg = FigureCanvasTkAgg(figure, canvas)
        mplCanvas = figAgg.get_tk_widget()
        # and connect figure with scrolling region
        cwid = canvas.create_window(0, 0, window=mplCanvas, anchor=Tkconstants.NW)
        changeSize(figure, 1)

    def changeSize(figure, factor):
        global canvas, mplCanvas, interior, interior_id, frame, cwid
        oldSize = figure.get_size_inches()
        figure.set_size_inches([factor * s for s in oldSize])
        wi, hi = [i * figure.dpi for i in figure.get_size_inches()]
        mplCanvas.config(width=wi, height=hi)
        canvas.itemconfigure(cwid, width=wi, height=hi)
        canvas.config(scrollregion=canvas.bbox(Tkconstants.ALL), width=200, height=200)
        for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                     ax.get_xticklabels() + ax.get_yticklabels()):
            item.set_fontsize(item.get_fontsize() * factor)
        ax.xaxis.labelpad = ax.xaxis.labelpad * factor
        ax.yaxis.labelpad = ax.yaxis.labelpad * factor
        figure.subplots_adjust(left=0.2, bottom=0.15, top=0.86)
        plt.tight_layout()
        figure.canvas.draw()

    global chat, time, user, new, figure, canvas
    words = text_W.get().strip()
    if words == "":
        messagebox.showinfo('warnning', 'words is empty')
        return
    if len(chat) == 0:
        messagebox.showinfo('warnning', 'chatting log is empty')
        return
    word = words.split()
    times = {}
    for i in range(0, len(time)):
        for j in range(0, len(word)):
            if word[j] in chat[i]:
                if time[i][:5] in times:
                    times[time[i][:5]] += 1
                else:
                    times[time[i][:5]] = 1
                break

    new = Toplevel()
    new.title('Graph')
    new.geometry('800x410')
    new.rowconfigure(1, weight=1)
    new.columnconfigure(1, weight=1)
    frame = Frame(new)
    frame.grid(column=1, row=1, sticky=Tkconstants.NSEW)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)
    term = len(list(times.keys()))
    plt.clf()
    figure = plt.figure(figsize=(term/6, 4))
    ax = figure.add_subplot(111)
    ax.plot(list(times.keys()), list(times.values()))
    start, end = ax.get_xlim()
    term /= 20
    if term > 5:
        term = 5
    ax.xaxis.set_ticks(np.arange(start, end, term))
    ax.set_xlabel('times')
    ax.set_ylabel('numbers')

    addScrollingFigure(figure, frame)
    plt.tight_layout()
    buttonFrame = Frame(new)
    buttonFrame.grid(row=1, column=2, sticky=Tkconstants.NS)
    biggerButton = Button(buttonFrame, text="larger",
                          command=lambda: changeSize(figure, 1.2))
    biggerButton.grid(column=1, row=1)
    smallerButton = Button(buttonFrame, text="smaller",
                           command=lambda: changeSize(figure, 0.833))
    smallerButton.grid(column=1, row=2)


if __name__ == "__main__":
    root = Tk()
    root["bg"] = "#777777"
    root.title('twitch analyzer')
    Frame1 = Frame(root, height=200, bg="#777777")
    title = Label(Frame1, text='twitch analyzer', bg="#777777")
    title.grid(row=0, column=0, padx=10, columnspan='6')
    title.config(font=('', 30,))
    lbl_V = Label(Frame1, text='Video_Id', bg="#777777", borderwidth=2, relief="solid", width=7)
    lbl_V.grid(row=1, column=0, padx=10, pady=10)
    text_V = Entry(Frame1, borderwidth=2, relief="solid")
    text_V.grid(row=1, column=1, padx=10, pady=10)
    lbl_C = Label(Frame1, text='Client_Id', bg="#777777", borderwidth=2, relief="solid", width=7)
    lbl_C.grid(row=1, column=2, padx=10, pady=10)
    text_C = Entry(Frame1, borderwidth=2, relief="solid")
    text_C.grid(row=1, column=3, padx=10, pady=10)
    lbl_W = Label(Frame1, text='Words', bg="#777777", borderwidth=2, relief="solid", width=7)
    lbl_W.grid(row=1, column=4, padx=10, pady=10)
    text_W = Entry(Frame1, borderwidth=2, relief="solid")
    text_W.grid(row=1, column=5, padx=10, pady=10)
    btn_A = Button(Frame1, text='Load', command=load, width=15)
    btn_A.grid(row=3, column=0, padx=10, pady=10, columnspan='3')
    btn_G = Button(Frame1, text='Graph', command=graph, width=15)
    btn_G.grid(row=3, column=3, padx=10, pady=10, columnspan='3')
    Frame1.pack(side=TOP, padx=10, pady=10)

    Frame2 = Frame(root, height=200, bg="#777777")
    lbl1 = Label(Frame2, text='Chat Log', bg="#777777")
    lbl1.pack(pady=10)
    lbl1.config(font=('', 20,))
    scroll1 = Scrollbar(Frame2)
    scroll2 = Scrollbar(Frame2, orient=HORIZONTAL)
    text_A = Listbox(Frame2, width=80, yscrollcommand=scroll1.set, xscrollcommand=scroll2.set, selectbackground="#333333")
    scroll2.pack(side=BOTTOM, fill=X)
    text_A.pack(side=LEFT, fill=Y)
    scroll1.pack(side=RIGHT, fill=Y)
    scroll1["command"] = text_A.yview
    scroll2["command"] = text_A.xview
    Frame2.pack(fill=Y, padx=10, pady=10)

    root.mainloop()
