# Click and hotkeys
import mouse, keyboard

# GUI for settings
import tkinter as tk
from tkinter import ttk, messagebox
# File management
import os
import json
import sys
# Audio indicators
from playsound import playsound

class AutoWindow:
    def __init__(self):
        # Tk init
        self.window = tk.Tk()
        self.window.iconbitmap(default='icon.ico')  
        self.window.title('AutoClicker')
        self.window.geometry('400x200')
        self.window.wm_iconbitmap('icon.ico')
        
        # AutoClick Hotkey
        keyboard.add_hotkey('ctrl+1',self.InvertClick)

        # Clicking
        self.Clicking = False
        self.SessionClicks = 0
        self.TotalClicks = 0

        # Stats
        self.CPSSessions = []
        self.BestSession = 0
        self.LastSession = 0

        self.windowElements = {
            'Session' : tk.Label(self.window),
            'Total' : tk.Label(self.window),
            'LastSessionLabel' : tk.Label(self.window),
            'ProgessLabel': tk.Label(self.window),
            'RecordBar' : ttk.Progressbar(self.window,length=380)
        }
        self.loadJson()

        for windowElm in self.windowElements.values():
            print(windowElm)
            windowElm.pack()
        
        try:
            self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)
            self.Update()
            self.window.mainloop()
        except Exception as e:
            messagebox.showerror('Exception',f'Exception: {e}')
            sys.exit()


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
        playsound('Audio\Copy.wav')

    def AutoClick(self):
        if self.Clicking:
            self.SessionClicks += 1
            self.TotalClicks += 1
            self.windowElements['Session'].config(text=f'Session Clicks: {self.SessionClicks}')
            self.windowElements['Total'].config(text=f'Total Clicks: {self.TotalClicks}')
            self.windowElements['ProgessLabel'].config(text=f'{self.SessionClicks}/{self.BestSession}')
            if self.windowElements['RecordBar']['value'] < 100:
                self.windowElements['RecordBar']['value'] = (self.SessionClicks/self.BestSession) * 100
                print(f"{self.windowElements['RecordBar']['value']}")
            mouse.click()

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
        self.AutoClick()
        self.window.after(1,self.Update)

# Main
def main():
    AutoWindow()

#/_________________________/START/_________________________/
if __name__ == "__main__":
    main()