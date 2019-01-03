import pandas
import numpy


def joinDatasets(understat, epl):
    #need to match names
    understat[['first_name','last_name']] = understat['player_name'].loc[understat['player_name'].str.split().str.len() == 2].str.split(expand=True)
    
    
    understat['last_name'] = numpy.where(understat['player_name']=='Johann Berg Gudmundsson' , 'Gudmundsson' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Patrick van Aanholt' , 'van Aanholt' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Jon Gorenc Stankovic' , 'Stankovic' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Jean Michael Seri' , 'Seri' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Kevin De Bruyne' , 'De Bruyne' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='David de Gea' , 'De Gea' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Virgil van Dijk' , 'van Dijk' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Maxime Le Marchand' , 'Le Marchand' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Bruno Ecuele Manga' , 'Manga' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Rajiv van La Parra' , 'van La Parra' , understat['last_name'])
    
    
    #Adjusting the understat names to match the weird names used by fpl
    understat['last_name'] = numpy.where(understat['player_name']=='David Luiz'   , 'David Luiz' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Steve Cook'   , 'Steve Cook' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Adam Smith'   , 'Adam Smith' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Bruno Ecuele Manga' , 'Ecuele Manga' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Cédric Soares'       , 'Cédric' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Kiko Femenía' , 'Kiko Femenía' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Romain Saiss', 'Saïss', understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Jazz Richards' , 'Jazz Richards' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='David Silva' , 'David Silva' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Son Heung-Min' , 'Son' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Bernardo Silva' , 'Bernardo Silva' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Felipe Anderson' , 'Felipe Anderson' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Lucas Moura' , 'Lucas Moura' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='André Gomes' , 'André Gomes' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Lewis Cook' , 'Lewis Cook' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Ki Sung-yueng' , 'Ki Sung-yueng' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Fousseni Diabate' , 'Diabaté' , understat['last_name'])
    #understat['last_name'] = numpy.where(understat['player_name']=='Zambo Anguissa' , 'Gudmundsson' , understat['last_name']) #Franck Zambo?
    understat['last_name'] = numpy.where(understat['player_name']=='Carlos Sánchez' , 'Carlos Sánchez' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Oriol Romeu' , 'Oriol Romeu' , understat['last_name'])
    understat['last_name'] = numpy.where(understat['player_name']=='Lucas Pérez' , 'Lucas' , understat['last_name'])
    
    
    
    #Players with one name are all that should be left now
    understat['last_name'] = numpy.where(understat['last_name'].isnull(), understat['player_name'], understat['last_name'])
    
    df = pandas.merge(epl, understat, how='left', left_on='Name', right_on='last_name')
    
    #filter na values
    df = df[df['red_cards'].notnull()]

    return(df)



