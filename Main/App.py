from tkinter import *
import ttkbootstrap as ttk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.ticker import StrMethodFormatter
from matplotlib.cm import ScalarMappable
import requests
import json
from tkinter.ttk import Progressbar
import os
import threading


cdict3 = {
    'red': (
        (0.0, 0.0, 0.0),
        (0.25, 0.0, 0.0),
        (0.5, 0.8, 1.0),
        (0.75, 1.0, 1.0),
        (1.0, 0.4, 1.0),
    ),
    'green': (
        (0.0, 0.0, 0.0),
        (0.25, 0.0, 0.0),
        (0.5, 0.9, 0.9),
        (0.75, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    ),
    'blue': (
        (0.0, 0.0, 0.4),
        (0.25, 1.0, 1.0),
        (0.5, 1.0, 0.8),
        (0.75, 0.0, 0.0),
        (1.0, 0.0, 0.0),
    )
}

cdict4 = {
    **cdict3,
    'alpha': (
        (0.0, 1.0, 1.0),
        # (0.25, 1.0, 1.0),
        (0.5, 0.3, 0.3),
        # (0.75, 1.0, 1.0),
        (1.0, 1.0, 1.0),
    ),
}

seasonGames = {
    'Regular season': 'R',
    'Post season': 'PR',
    'All Games': 'A'
}


class App(tk.Tk):
    def __init__(self):
        self.seasons = ['2022-2023', '2022-2023', '2021-2022', '2020-2021', '2019-2020']
        self.season = '2022-2023'
        super().__init__()
        Frame(self)
        ttk.Style("yeti")
        self.directory_path = os.path.dirname(__file__)
        file_path = os.path.join(self.directory_path,"./img/puck.ico")
        self.title("Stat my Hockey")
        self.iconbitmap(file_path)
        self.geometry("1065x600")

        self.option_var = tk.StringVar(self)
        self.awayoption_var = tk.StringVar(self)
        self.season_var = tk.StringVar(self)

        self.homeShoots = []
        self.homeShootsX = []
        self.homeShootsY = []
        self.homeGoals = []
        self.homeGoalsX = []
        self.homeGoalsY = []
        self.awayShoots = []
        self.awayShootsX = []
        self.awayShootsY = []
        self.awayGoals = []
        self.awayGoalsX = []
        self.awayGoalsY = []
        self.games = []

        self.awayStatShots_label = ttk.Label(self,bootstyle="dark")
        self.awayStatGoals_label = ttk.Label(self,bootstyle="dark")
        self.awayStatBlocks_label = ttk.Label(self,bootstyle="dark")
        self.awayStatHits_label = ttk.Label(self,bootstyle="dark")


        self.homeStatShots_label = ttk.Label(self,bootstyle="dark")
        self.homeStatGoals_label = ttk.Label(self,bootstyle="dark")
        self.homeStatBlocks_label = ttk.Label(self,bootstyle="dark")
        self.homeStatHits_label = ttk.Label(self,bootstyle="dark")
        self.hometeam_label = ttk.Label(self,bootstyle="dark")
        self.awayteam_label = ttk.Label(self,bootstyle="dark")
        self.awayHits = 0
        self.awayBlocks = 0
        self.homeHits = 0
        self.homeBlocks = 0
        self.setupOptions()
        self.setupOptionsMenus()
        self.setupCheckBoxes()
        self.initColorMaps()

        pass

    def setupOptions(self):
        response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
        type(response.text)
        self.configure(bg='white')
        json_object = json.loads(response.text)
        self.teams = {0: 'Home'}
        self.awayteams = {0: 'Away'}
        for x in json_object['teams']:
            self.teams[x['id']] =  x['teamName']
            self.awayteams[x['id']] = x['teamName'] 
        pass
    
    def initColorMaps(self):
        ncolors = 256
        home_array = plt.get_cmap('summer_r')(range(ncolors))
        goal_array = plt.get_cmap('Wistia')(range(ncolors))
        awaycolor_array = plt.get_cmap('winter_r')(range(ncolors))

        home_array[:,-1] = np.linspace(0.0,1.0,ncolors)
        goal_array[:,-1] = np.linspace(0.0,1.0,ncolors)
        awaycolor_array[:,-1] = np.linspace(0.0,1.0,ncolors)
        map_object = LinearSegmentedColormap.from_list(name='homeclr',colors=home_array)
        plt.colormaps.register(map_object)
        map_object = LinearSegmentedColormap.from_list(name='goalclr',colors=goal_array)
        plt.colormaps.register(map_object)
        map_object = LinearSegmentedColormap.from_list(name='awayclr',colors=awaycolor_array)
        plt.colormaps.register(map_object)
        pass

    def setupOptionsMenus(self):
        homeTeam = ttk.OptionMenu(
                self,
                self.option_var,
                *self.teams.values(),
                command=self.option_changed)
        
        homeTeam.place(x=5, y=50)
        self.output_label = ttk.Label(self, bootstyle="dark")
        self.output_label.place(x=5, y=80)

        awayTeam = ttk.OptionMenu(
                self,
                self.awayoption_var,
                *self.awayteams.values(),
                command=self.awayoption_changed)
        awayTeam.place(x=5, y=120)
        
        self.awayoutput_label = ttk.Label(self,bootstyle="dark")
        self.awayoutput_label.place(x=5, y=150)

        seasons = ttk.OptionMenu(
                self,
                self.season_var,
                *self.seasons,
                command=self.seasonoption_changed)
        seasons.place(x=5, y=210)
        
        self.season_label = ttk.Label(self,bootstyle="dark")
        self.season_label.place(x=5, y=250)

   
        pass

    def setupCheckBoxes(self):
        self.rdbtngames = ttk.StringVar()
        yval = 260        
        for (text, value) in seasonGames.items():
            rdButton = ttk.Radiobutton(self, text=text, variable=self.rdbtngames, value=value, command=self.gameTypeChanged)
            yval += 30
            rdButton.place(x=5, y=yval)
            if value == 'R':
                rdButton.invoke()
        pass

    def option_changed(self, *args):
        self.hometeam = self.option_var.get()
        self.output_label['text'] = f'Home team: {self.option_var.get()}'
        self.searchForData()
        pass

    def awayoption_changed(self, *args):
        self.awayteam = self.awayoption_var.get()
        self.awayoutput_label['text'] = f'Away team: {self.awayoption_var.get()}'
        self.searchForData()
        pass

    def seasonoption_changed(self, *args):
        self.season = self.season_var.get()
        self.season_label['text'] = f'Season: {self.season_var.get()}'
        self.searchForData()
        pass

    def gameTypeChanged(self, *args):
        self.searchForData()
        pass

    def searchForData(self):
        if self.output_label['text'] != '' and  self.awayoutput_label['text'] != '':
            progress_var= Progressbar(self,orient=HORIZONTAL,length=200,mode='indeterminate')
            progress_var.start()
            progress_var.place(x=500, y=300)
            homeTeamId = [i for i in self.teams if self.teams[i] == self.hometeam]
            awayTeamId = [i for i in self.awayteams if self.awayteams[i] == self.awayteam]
            self.getGames(str(homeTeamId[0]), str(awayTeamId[0]))
            self.getData(homeTeamId[0], awayTeamId[0])
            self.createCParam()
            self.displayHockeyRink()
            progress_var.destroy()
            self.clearLists()
        pass

    def displayHockeyRink(self):
        file_path = os.path.join(self.directory_path,"./img/hrink.png")
        img = plt.imread(file_path)
        fig, ax = plt.subplots()
        ax, fig.set_size_inches(8, 6)
        x = np.arange(-105.0, 105.0)
        y = np.arange(-52.0, 52.0)
        ax.set_xlim([-105, 105])
        ax.set_ylim([-52, 52])
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
        plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) # No decimal places
        extent = np.min(x), np.max(x), np.min(y), np.max(y)

        fig.suptitle(self.hometeam + ' vs. ' + self.awayteam, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.imshow(img, zorder=0, extent=extent)
        # home = plt.imshow(Z3, cmap='homeclr', alpha=1, interpolation='gaussian',
        #                 extent=extent) 
        plt.scatter(self.homeShootsX, self.homeShootsY, c=self.homeShotsC, s=30, cmap="winter")
        # away = plt.imshow(Z4, cmap='awayclr', alpha=1, interpolation='none',
        #                 extent=extent) 
        plt.scatter(self.awayShootsX, self.awayShootsY, c=self.awayShootsC, s=30, cmap="winter")
        # homegoal = plt.imshow(Z5, cmap='goalclr', alpha=1, interpolation='none',
        #                 extent=extent)        
        plt.scatter(self.homeGoalsX, self.homeGoalsY, c=self.homeGoalsC, s=30, cmap="autumn") 
        # awaygoal = plt.imshow(Z6, cmap='goalclr', alpha=1, interpolation='none',
        #                 extent=extent)   
        plt.scatter(self.awayGoalsX, self.awayGoalsY, c=self.awayGoalsC, s=30, cmap="autumn") 
        # plt.show()
        canvas = FigureCanvasTkAgg(fig,
                                master = self)  
        canvas.draw()
        canvas.get_tk_widget().place(x=160, y=5)
        self.displayAwayStats()
        self.displayHomeStats()
        pass

    def createCParam(self):
        self.homeShotsC = [1] * len(self.homeShoots) 
        self.homeGoalsC = [1] * len(self.homeGoals)
        self.awayShootsC = [1] * len(self.awayShoots) 
        self.awayGoalsC = [1] * len(self.awayGoals)
        if len(self.homeGoals) != 0:
            self.homeGoalsC = [self.homeGoals.count(x) for x in self.homeGoals]

        self.homeShotsC = [self.homeShoots.count(x) for x in self.homeShoots]

        if len(self.awayGoals) != 0:
            self.awayGoalsC = [self.awayGoals.count(x) for x in self.awayGoals]
        
        self.awayShootsC = [self.awayShoots.count(x) for x in self.awayShoots]

        pass

    def getGames(self, homeTeamId, awayTeamId):
        season = ''
        if self.season == "2022-2023":
            season = '20222023'
        elif self.season == "2021-2022":
            season = '20212022'
        elif self.season == "2020-2021":
            season = '20202021'
        elif self.season == "2019-2020":  
            season = '20192020'
        else:
            season = '20222023'

        response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?season=" + season + "&teamId=" + homeTeamId)
        type(response.text)
        json_object = json.loads(response.text)
        value = self.rdbtngames.get() 
        self.games = [x['games'][0] for x in json_object['dates'] if x['games'][0]['teams']['away']['team']['id'] == int(awayTeamId)
                    or (x['games'][0]['teams']['away']['team']['id'] == int(homeTeamId)
                    and x['games'][0]['teams']['home']['team']['id'] == int(awayTeamId)) 
                    if (x['games'][0]['gameType'] == value or value == 'A')]

        # for x in games:
        #     if value == 1 and x['games'][0]['gameType'] == 'R':
        #         self.games.append(x['games'][0])
        #     elif value == 2 and x['games'][0]['gameType'] == 'P':
        #         self.games.append(x['games'][0])
        #     elif value == 3:
        #         self.games.append(x['games'][0])
        pass

    def getData(self, homeId, awayId):
        for x in self.games:
            response = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(x['gamePk']) + "/feed/live")
            type(response.text)
            game = json.loads(response.text)
            homeevents = [x for x in game['liveData']['plays']['allPlays'] if "team" in x 
                      and x['team']['id'] == homeId
                      and (x['result']['event'] == 'Shot' or x['result']['event'] == 'Goal' 
                           or x['result']['event'] == 'Hit' or x['result']['event'] == 'Blocked Shot')]
            awayevents= [x for x in game['liveData']['plays']['allPlays'] if "team" in x 
                        and x['team']['id'] == awayId
                        and (x['result']['event'] == 'Shot' or x['result']['event'] == 'Goal' 
                           or x['result']['event'] == 'Hit' or x['result']['event'] == 'Blocked Shot')] 
            
            for y in awayevents:
                if y['result']['event'] == 'Shot':
                    coord = y['coordinates']
                    coord['x'] = abs(coord['x'])
                    self.awayShoots.append(coord)
                    self.awayShootsX.append(coord['x'])
                    self.awayShootsY.append(coord['y'])
                elif y['result']['event'] == 'Goal':
                    coord = y['coordinates']
                    coord['x'] = abs(coord['x'])
                    self.awayGoals.append(coord)
                    self.awayGoalsX.append(coord['x'])
                    self.awayGoalsY.append(coord['y'])
                elif  y['result']['event'] == 'Hit':
                    self.awayHits += 1
                elif  y['result']['event'] == 'Blocked Shot':
                    self.awayBlocks += 1

            for y in homeevents:
                if y['result']['event'] == 'Shot':
                    coord = y['coordinates']
                    coord['x'] = -abs(coord['x'])
                    self.homeShoots.append(coord)
                    self.homeShootsX.append(coord['x'])
                    self.homeShootsY.append(coord['y'])
                elif y['result']['event'] == 'Goal':
                    coord = y['coordinates']
                    coord['x'] = -abs(coord['x'])
                    self.homeGoals.append(coord)
                    self.homeGoalsX.append(coord['x'])
                    self.homeGoalsY.append(coord['y'])
                elif  y['result']['event'] == 'Hit':
                    self.homeHits += 1
                elif y['result']['event'] == 'Blocked Shot':
                    self.homeBlocks += 1
                    

        pass

    def displayHomeStats(self):
        self.hometeam_label['text'] = f'{self.hometeam}:'
        self.hometeam_label.place(x=965, y=50)
        self.homeStatShots_label['text'] = f'Shots: {len(self.homeShoots)}'
        self.homeStatShots_label.place(x=965, y=80)

        self.homeStatGoals_label['text'] = f'Goals: {len(self.homeGoals)}'
        self.homeStatGoals_label.place(x=965, y=95)

        self.homeStatBlocks_label['text'] = f'Blocked Shots: {self.homeBlocks}'
        self.homeStatBlocks_label.place(x=965, y=110)

        self.homeStatHits_label['text'] = f'Hits: {self.homeHits}'
        self.homeStatHits_label.place(x=965, y=125)

        pass

    def displayAwayStats(self):
        self.awayteam_label['text'] = f'{self.awayteam}:'
        self.awayteam_label.place(x=965, y=360)

        self.awayStatShots_label['text'] = f'Shots: {len(self.awayShoots)}'
        self.awayStatShots_label.place(x=965, y=390)

        self.awayStatGoals_label['text'] = f'Goals: {len(self.awayGoals)}'
        self.awayStatGoals_label.place(x=965, y=405)

        self.awayStatBlocks_label['text'] = f'Blocked Shots: {self.awayBlocks}'
        self.awayStatBlocks_label.place(x=965, y=420)

        self.awayStatHits_label['text'] = f'Hits: {self.awayHits}'
        self.awayStatHits_label.place(x=965, y=435)

        pass

    def clearLists(self):
        del self.awayGoals[:]
        del self.awayGoalsX[:]
        del self.awayGoalsY[:]

        del self.homeGoals[:]
        del self.homeGoalsX[:]
        del self.homeGoalsY[:]

        del self.awayShoots[:]
        del self.awayShootsX[:]
        del self.awayShootsY[:]

        del self.homeShoots[:]
        del self.homeShootsX[:]
        del self.homeShootsY[:]

        del self.games[:]
        self.awayHits = 0
        self.awayBlocks = 0
        self.homeHits = 0
        self.homeBlocks = 0

        pass


if __name__ == '__main__':

    app = App()
    app.mainloop()