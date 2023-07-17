# Click and hotkeys
import mouse, keyboard

# GUI for settings
import tkinter as tk
from tkinter import ttk, messagebox
import ttkthemes

# File management
import os
import json
import sys

# Audio indicators
from playsound import playsound

# To Buy upgrades and find cookies
import AutoUI
import pyautogui

# Threading to speed up the number of clicks
from threading import Thread


class AutoWindow:
    def __init__(self):
        # Tk init
        self.window = ttkthemes.ThemedTk(theme='equilux')
        self.window.resizable(False,False)
        self.window.configure(bg='#464646')
        self.window.iconbitmap(default='icon.ico')  
        self.window.title('AutoClicker')
        self.window.wm_iconbitmap('icon.ico')
        
        # AutoClick Hotkey
        keyboard.add_hotkey('ctrl+1',self.InvertClick)

        # Sound Thread
        self.soundPlayer = Thread()

        # Clicking
        self.Clicking = False
        self.SessionClicks = 0
        self.TotalClicks = 0

        # Stats
        self.CPSSessions = []
        self.BestSession = 0
        self.LastSession = 0

        # How often to search screen for upgrades in milliseconds
        self.Searchinverval = 1000
        self.Elapsedtime = 0
        self.AutoBuy = tk.IntVar(self.window)

        self.windowElements = {
            'Session' : ttk.Label(self.window),
            'Sep1' : ttk.Separator(self.window,orient='horizontal'),
            'Total' : ttk.Label(self.window),
            'LastSessionLabel' : ttk.Label(self.window),
            'ProgessLabel': ttk.Label(self.window),
            'RecordBar' : ttk.Progressbar(self.window,length=380),
            'AutoBuy' : ttk.Checkbutton(self.window,text='AutoBuy',var=self.AutoBuy,onvalue=1,offvalue=0,command=self.SetAutobuy),
            'BuyIntervalLabel': ttk.Label(self.window,text='Buy Interval (ms):'),
            'BuyInterval' : ttk.Scale(self.window,from_=50,to=1000,orient='horizontal',length=350,)
        }


        self.loadJson()

        for windowElm in self.windowElements.values():
            # print(windowElm)
            windowElm.pack()
        
        # Makes geometry fit i think
        # 200x200+190+190
        self.window.geometry('400x250+0+0')

        
        try:
            self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
            self.Update()
            self.window.mainloop()
        except Exception as e:
            messagebox.showerror('Exception',f'Exception: {e}')
            sys.exit()

    def SetAutobuy(self):
        self.Searchinverval = self.windowElements['BuyInterval'].get()
        SE('Audio\AutoBuy.mp3')
        print(self.Searchinverval)
        print(self.AutoBuy.get())

    def loadJson(self):
        if not os.path.exists('stats.json'):
            # CPS stores a new Dict per session, so I can put it into matplotlib and see how much I have clicked later on
            stats = {
                'CPS' : {
                    1:0
                },
                'Total_Clicks': 0,
                'Time_Clicked': 0
            }
            with open('stats.json','w') as jsonFile:
                json.dump(stats,jsonFile,ensure_ascii=True)
            jsonFile.close()
        else:
            with open('stats.json','r') as jsonFile:
                stats = json.load(jsonFile)
                self.TotalClicks = stats['Total_Clicks']
                self.CPSSessions = [key for key in stats['CPS'].values()]
                self.BestSession = max(self.CPSSessions)
                self.LastSession = self.CPSSessions[-1]
            jsonFile.close()
            self.windowElements['Total'].config(text=f'Total Clicks: {self.TotalClicks}')

            self.windowElements['LastSessionLabel'].config(text=f'Last Session: {self.LastSession}')

            self.windowElements['Session'].config(text=f'Session Clicks: {self.SessionClicks}')
            self.windowElements['ProgessLabel'].config(text=f'{self.SessionClicks}/{self.BestSession}')

    def InvertClick(self):
        self.Clicking = not self.Clicking
        print(f'AutoBuy: {self.AutoBuy}')
        playsound('Audio\Copy.wav')

    def AutoClick(self):
        if self.Clicking:
            self.SessionClicks += 1
            self.TotalClicks += 1
            self.windowElements['Session'].config(text=f'Session Clicks: {self.SessionClicks}')
            self.windowElements['Total'].config(text=f'Total Clicks: {self.TotalClicks}')
            self.windowElements['ProgessLabel'].config(text=f'{self.SessionClicks}/{self.BestSession}')
            if self.BestSession > 0:
                if self.windowElements['RecordBar']['value'] < 100:
                    self.windowElements['RecordBar']['value'] = (self.SessionClicks/self.BestSession) * 100
            else:
                self.windowElements['RecordBar']['value'] = 100
            mouse.click()

    def AutoUpgrade(self):
        if self.Clicking:
            self.Elapsedtime +=1
            if self.Elapsedtime >= self.Searchinverval:
                print('searching')
                LastMousePos = mouse.get_position()
                self.Elapsedtime = 0
                # AutoBuy
                # TODO: Needs Reversing
                if self.AutoBuy.get():
                    print(self.Elapsedtime)
                    AutoUI.PressUpgrade()
                    pyautogui.moveTo(LastMousePos)


    # Exit window and save Json data
    def closeWindow(self):
        print('Quitting')
        try:
            # read current json
            with open('stats.json','r') as jsonFile:
                stats = json.load(jsonFile)
            jsonFile.close()

            stats['CPS'][len(stats['CPS']) + 1] = self.SessionClicks
            stats['Total_Clicks'] += self.SessionClicks

            # write new stats
            with open('stats.json','w') as jsonFile:
                json.dump(stats,jsonFile,ensure_ascii=True)
            jsonFile.close()

            print(f'Wrote to json')
        except Exception as e:
            print(e)
            print('failed to write')
        self.window.destroy()

    def Update(self):
        self.AutoUpgrade()
        self.AutoClick()
        self.AutoClick()
        self.window.after(1,self.Update)

# Main
def main():
    AutoWindow()

# To be used in a thread, so it doesnt stop usability
def SE(effect):
    soundThread = Thread(target=playsound,args=(str(effect),))
    soundThread.start()

#/_________________________/START/_________________________/
if __name__ == "__main__":
    
    main()

print('not hi')