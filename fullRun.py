import getFPL
import parseFPL
import parseUnderstat
import joinData 
import varAdd
import os

#TODO
#Merge together joinData and varAdd into one file
#make the optimiser more flexible

if not os.path.exists('html'):
        os.makedirs('html')

if not os.path.exists('data'):
        os.makedirs('data')

#get the websites
saveSite("https://fantasy.premierleague.com/player-list/", "html/FPLPoints.html")
saveSite("https://understat.com/league/EPL", "html/understatEPL.html")


#parse the  html into a dataframe
epl = parseFPL.getFPlPlayers(path = "html/FPLPoints.html")
epl.to_pickle("data/FPL.pkl")
#print(df)
understat = parseUnderstat.getUnderstatPlayers(path = "html/understatEPL.html")
understat.to_pickle("data/Understat.pkl")

#understat = pandas.read_pickle("Understat.pkl")
#epl       = pandas.read_pickle("FPL.pkl")
#join the two datasets together
df = joinData.joinDatasets(understat, epl)
df.to_pickle("data/Dataset.pkl")

#data = pandas.read_pickle("Dataset.pkl")

#calculate some extra variables and run the optimiser
data = varAdd.calcExtraVars(df)
result = varAdd.runOptimiser(data)

#result.to_pickle("data/Result.pkl")
result.to_pickle("data/Result352.pkl")

