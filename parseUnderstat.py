import ast
from bs4 import BeautifulSoup
import pandas


def getUnderstatPlayers(path = "understatEPL.html"):
    #really horrendous code to get the JSON object from Understat html
    #I am bad at web scraping
    myfile = open(path)
    soup = BeautifulSoup(myfile, 'html.parser')
    tmp = list(soup.children)
    data = tmp[2].find_all('script')
    thelist = data[3].text.split('=')[1].strip(';')
    json_stuff = thelist.replace("JSON.parse(", "{").replace(");\n", "}") 
    mydict = json_stuff.encode('utf-8').decode('unicode_escape')
    
    player_obj = ast.literal_eval(mydict[4:len(mydict)-3])
    
    #want to get 
    #player_name
    #team_title
    #time
    #xG
    #goals
    #npxG
    #npg
    #assists
    #xA
    #yellow cards
    #red_Cards


    #turn the JSON into a data frame
    #This is a not very efficient way
    #See here for speed up if necessary
    #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.append.html
    df = pandas.DataFrame(columns = ['player_name', 'team_title',
                                     'time', 'xG', 'goals',
                                     'npxG', 'npg',
                                     'assists', 'xA',
                                     'yellow_cards', 'red_cards'
                                     ])
    
    for player in player_obj:
        #print(player['player_name'])
        df=df.append({
            'player_name': player['player_name'], 
            'team_title':player['team_title'],
            'time':player['time'],
            'xG':player['xG'], 
            'goals':player['goals'],
            'npxG':player['npxG'], 
            'npg':player['npg'],
            'assists':player['assists'], 
            'xA':player['xA'],
            'yellow_cards':player['yellow_cards'], 
            'red_cards':player['red_cards']
            },
            ignore_index=True
                )


    return(df)
    
    
    #df2 = pandas.read_pickle("Understat.pkl")
    
    #What the JSON looks like for each player
    #{'position': 'F M S'
    # 'time': '1315'
    # 'goals': '10'
    # 'yellow_cards': '0'
    # 'xGChain': '11.44818026944995'
    # 'team_title': 'Arsenal'
    # 'xG': '8.5520558077842'
    # 'red_cards': '0'
    # 'assists': '3'
    # 'shots': '40'
    # 'npxG': '7.790886910632253'
    # 'id': '318'
    # 'player_name': 'Pierre-Emerick Aubameyang'
    # 'npg': '9'
    # 'games': '17'
    # 'xA': '2.668694654479623'
    # 'key_passes': '17'
    # 'xGBuildup': '2.9089619740843773'}
