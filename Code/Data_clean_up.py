###################
## Data clean up ##
###################

import pandas as pd

# ---- Import data : outputs form scrapping ---- #

General = pd.read_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Overall_info.csv', encoding="utf-8-sig")
Votes = pd.read_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Votes.csv', encoding="utf-8-sig")
Abs = pd.read_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Abstentions.csv', encoding="utf-8-sig")
Descrip = pd.read_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\raw\Description.csv', encoding="utf-8-sig")

# --------------------------------- Clean up data ----------------------------------------------- #


# --------------------- General Dataset on bills ------------------------------ #

## Join data abstentions and votes in a single dataframe
Voting = Votes.append(Abs) 

## Create vote dummies
vote_dummies = pd.get_dummies(Voting['voto'])
Voting = pd.concat([Voting, vote_dummies], axis=1)      

## Correct general info for those without summary the info on the on page
simple_vote = Voting[['vote_link','Abstencion', 'Aprobado', 'Rechazado' ]]
### Summary data (votes group by bill)
votes_sum = simple_vote.groupby('vote_link', as_index=False).sum()
votes_sum['Votoss'] = votes_sum['Aprobado'] + votes_sum['Rechazado']
### replace missing data 
General_new = pd.merge(General, votes_sum, how='outer', on='vote_link')
General_new['Votoss'].fillna(General_new['Votos'], inplace=True)
General_new['Abstencion'].fillna(General_new['Absenciones'], inplace=True)

## Add missing camara info using comision
General_new.loc[General_new['Comision'].str.contains('Cámara'), 'Camara'] = [['Cámara de Representantes']]
General_new.loc[General_new['Comision'].str.contains('Senado'), 'Camara'] = [['Senado']]
General_new.loc[General_new['Comision'].str.contains('Cámara') & General_new['Comision'].str.contains('Senado'), 'Camara'] = [['Cámara de Representantes-Senado']]

## Add description info to bills (description, author, parties)
General_new = pd.merge(General_new, Descrip, how='right', on='vote_link')

## Let's gen a simple id by bill
General_new['id'] = range(1, len(General_new) + 1)

## Define dates

### Clean up string
General_new['Date'] = General_new['Date'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
General_new['Date'] = General_new['Date'].map(lambda x: x.replace('d', ''))
General_new['Date'] = General_new['Date'].map(lambda x: x.replace(' ', '/'))
General_new['Date'] = General_new['Date'].map(lambda x: x.replace('//', '/'))
### Change letters to month number 
months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
m_num = 0
for i in months:
    m_num = m_num + 1
    General_new['Date'] = General_new['Date'].map(lambda x: x.replace(i, str(m_num)))
### Define date format
General_new["date"]= pd.to_datetime(General_new["Date"], format="%m/%d/%Y")

## Clean up strings 
General_new['Nombre:'] = General_new['Nombre:'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
General_new['Tipo'] = General_new['Tipo'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
General_new['Comision'] = General_new['Comision'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
General_new['Camara'] = General_new['Camara'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
General_new['tags'] = General_new['tags'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
General_new['tags'] = General_new['tags'].map(lambda x: x.replace('\'', ''))


## drop unneded columns
General_new = General_new.drop(columns=['Votos', 'Absenciones', 'click', 'Unnamed: 0_y', 'Unnamed: 0_x' ])

## renaming variables
General_new = General_new.rename(columns={"Nombre:": "Nombre", "Votoss": "Votos"})


## save clean General data
General_new.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\Clean\General.csv', encoding="utf-8-sig")

# --------------------- Vote Dataset : Votes per congressperson  ------------------------------ #

## Quick clean up of data

### Clean up strings 
Voting['Nombre:'] = Voting['Nombre:'].map(lambda x: x.lstrip('\'[').rstrip(']\''))
### drop unneded columns
Voting = Voting.drop(columns=['Unnamed: 0'])

## Add General info on the bills
Voting_new = pd.merge(Voting, General_new, how='left', on='vote_link')

## Renaming variables
Voting_new = Voting_new.rename(columns={"Abstencion_x": "Abstencion", "Aprobado_x": "Aprobado", "Rechazado_x": "Rechazado",
                                        "Abstencion_y": "Abstencion_tot", "Aprobado_y": "Aprobado_tot", "Rechazado_y": "Rechazado_tot",
                                        "Nombre_x": "Nombre"})

# dummy if voted or not
Voting_new['Voto_d'] = Voting_new['Aprobado'] + Voting_new['Rechazado']


## save clean
Voting_new.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\Clean\Voting.csv', encoding="utf-8-sig")








