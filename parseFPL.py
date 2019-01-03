from bs4 import BeautifulSoup
import numpy
import pandas
#Maybe only import part of pandas?


def makePlayerFrame(fplPlayers, pos="Unknown"):
    out = []
    for x in fplPlayers:
        #strip <td> and </td> here? 
        tmp = str(x).replace("<td>", "") 
        out.append(tmp.replace("</td>", ""))
    
    playerDict = dict(Name  = out[0::4], Team  = out[1::4], Points= list(map(int, out[2::4])), Value = out[3::4])

    players = pandas.DataFrame(playerDict)
    players = players.assign(Position=pos)
    return(players)


def getFPlPlayers(path = "FPLPoints.html"):


    #path = "FPLPoints.html"
    myfile = open(path,'r')
    soup = BeautifulSoup(myfile, 'html.parser')
    
    #3,9 = GK
    #11= header
    #13,19 = def
    #21= header
    #23,29 = mid
    #31= header
    #33,39 = forward
    
    
    #Get all the players
    GK1 = list(soup.children)[3].find_all('td')
    GK2 = list(soup.children)[9].find_all('td')
    def1 = list(soup.children)[13].find_all('td')
    def2 = list(soup.children)[19].find_all('td')
    Mid1 = list(soup.children)[23].find_all('td')
    Mid2 = list(soup.children)[29].find_all('td')
    fw1 = list(soup.children)[33].find_all('td')
    fw2 = list(soup.children)[39].find_all('td')
    
    
    #Convert each html table to a data frame and add position
    df_GK1 = makePlayerFrame(GK1, "Goalkeeper")
    df_GK2 = makePlayerFrame(GK2, "Goalkeeper")
    
    df_def1 = makePlayerFrame(def1, "Defender")
    df_def2 = makePlayerFrame(def2, "Defender")
    
    
    df_Mid1 = makePlayerFrame(Mid1, "Midfielder")
    df_Mid2 = makePlayerFrame(Mid2, "Midfielder")
    
    df_fw1 = makePlayerFrame(fw1, "Forward")
    df_fw2 = makePlayerFrame(fw2, "Forward")
    
    #Combine all into one dataframe
    frames = [df_GK1, df_GK2, df_def1, df_def2, df_Mid1, df_Mid2, df_fw1, df_fw2]
    df_Players = pandas.concat(frames)


#Add a column where the value is an numeric type?

    return(df_Players)


#def main():
#    df = getFPlPlayers(path = "FPLPoints.html")
#    #save the data frame
#    df.to_pickle("FPL.pkl")
#    print(df)
#        
#if __name__== "__main__":
#    main()


#f = open('foo.py')
#source = f.read()
#exec(source)
#print bar()
