import pandas
import numpy
from pulp import *




def calcExtraVars(data):

    #####TODO#####
    ###Make me a function?#####
    ###Write script to automate the whole process from web scraping to optimiser##
    ###Write variation of methodology that only selects the first team###
    
    
    
    #understat[['first_name']] = understat['player_name'].loc[understat['player_name'].str.split().str.len() == 2].str.split(expand=True)
    
    
    #########Create xPts from the points, goals, xG etc.########
    ######xPts is just points but with goals and assists replaced with their expected counterpart
    ######maybe change method?
    
    #data['goalxPts'] = numpy.where(data['Position']=='Goalkeeper' , 6, numpy.where(data['Position']=='Defender', 6, numpy.where(data['Position']=='Midfielder', 5, data['Position']=='Forward', 4, -1)))
    data['goalPts'] = numpy.where(data['Position']=='Goalkeeper' , 6, numpy.where(data['Position']=='Defender', 6, numpy.where(data['Position']=='Midfielder', 5, numpy.where(data['Position']=='Forward', 4, -1))))
    
    #make everything numeric
    data['xG'] = pandas.to_numeric(data['xG'])
    data['xA'] = pandas.to_numeric(data['xA'])
    data['red_cards'] = pandas.to_numeric(data['red_cards'])
    data['yellow_cards'] = pandas.to_numeric(data['yellow_cards'])
    data['Points'] = pandas.to_numeric(data['Points'])
    data['goals'] = pandas.to_numeric(data['goals'])
    data['assists'] = pandas.to_numeric(data['assists'])
    
    #calculate the points that dont come from goals etc.
    data['appearance_pts'] = (data.Points) - (data.goals*data.goalPts) - (data.assists*3)
    
    #Add on the expected points so we have adjusted the total points to match xG and xA
    
    #Add on the expected points so we have adjusted the total points to match xG and xA
    data['xPts'] = data.appearance_pts+(data.goalPts*data.xG)+(data.xA*3)
    data['xPtsDiff'] = data.xPts - data.Points
    #data['xPts'] = (data.goalPts*data.xG)+(data.xA*3)+(data.red_cards*-3)+(data.yellow_cards*-1) 
    
    #######Create flags for optimiser#######
    
    data['GK_flag'] = numpy.where(data['Position']=='Goalkeeper' , 1, 0) 
    data['Def_flag'] = numpy.where(data['Position']=='Defender' , 1, 0) 
    data['Mid_flag'] = numpy.where(data['Position']=='Midfielder' , 1, 0) 
    data['FW_flag'] = numpy.where(data['Position']=='Forward' , 1, 0) 
    #data['flag'] = 1 
    data['Value_num'] = data['Value'].map(lambda x: x.lstrip('£'))
    data['Value_num'] = pandas.to_numeric(data['Value_num'])

    return(data)



def runOptimiser(data):#find a way to make data.xPts a var passed into the function

    ######Make dictionarise for the optimiser######
    
    #maximise
    #pt_dict = dict(zip(data.Name, data.Points))  
    pt_dict = dict(zip(data.Name, data.xPts))  
    
    #player constraints
    gk_dict = dict(zip(data.Name, data.GK_flag))   #==2
    def_dict = dict(zip(data.Name, data.Def_flag)) #==5
    mid_dict = dict(zip(data.Name, data.Mid_flag)) #==5
    fw_dict = dict(zip(data.Name, data.FW_flag))   #==3
    
    #cost constraing
    price_dict = dict(zip(data.Name, data.Value_num)) # <=100
    
    #List of possible players
    players = list(data['Name'])
    
    
    
    #15.8
    #16
    
    
    prob = LpProblem("The FPL Problem", LpMaximize)
    player_vars = LpVariable.dicts("Play",players,cat="Binary")
    
    # The objective function is added to 'prob' first
    prob += lpSum([pt_dict[i]*player_vars[i] for i in players]), "Total Value of player"
    #Value constraint
    prob += lpSum([price_dict[i] * player_vars[i] for i in players]) <= 84, "PriceSum"
    prob += lpSum([gk_dict[i] * player_vars[i] for i in players])    == 1, "GKSum"
    prob += lpSum([def_dict[i] * player_vars[i] for i in players])   == 3, "DefSum"
    prob += lpSum([mid_dict[i] * player_vars[i] for i in players])   == 5, "MidSum"
    prob += lpSum([fw_dict[i] * player_vars[i] for i in players])    == 2, "FwSum"
    
    #prob += lpSum([price_dict[i] * player_vars[i] for i in players]) <= 83.5, "PriceSum"
    #prob += lpSum([gk_dict[i] * player_vars[i] for i in players])    == 1, "GKSum"
    #prob += lpSum([def_dict[i] * player_vars[i] for i in players])   == 4, "DefSum"
    #prob += lpSum([mid_dict[i] * player_vars[i] for i in players])   == 4, "MidSum"
    #prob += lpSum([fw_dict[i] * player_vars[i] for i in players])    == 2, "FwSum"
    
    prob.solve()
    
    #Get the results
    result = []
    for v in prob.variables():
        if(v.varValue == 1.0):
            result.append(v.name)
    
    result = [x.replace('Play_', '').replace('_', ' ') for x in result]
    data_result = data[data.Name.isin(result)]
    
    #maybe return result rather than data_result?
    return(data_result)

    #data_result.to_pickle("OptimTeam.pkl")
    
    #rules
    #-----
    #2 goalkeepers
    #5 defenders
    #5 midfielders
    #3 forwards
    #
    #value = £100m
    #max 3 players from 1 team
    
    
    #goal scored pts
    #--------------
    #gk=6
    #def=6
    #mid=5
    #fw =4
    #
    #assist=3
    #red card=-3
    #yellow=-1
    
    
    #min values
    #----------
    #GK 4.0
    #Def 3.8
    #Mid 4.3
    #Fw 4.4
    
    #tot =16.5
    #100-16.5=83.5
