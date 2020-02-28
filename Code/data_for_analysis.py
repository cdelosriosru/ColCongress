##############
## Analysis ##
##############

import pandas as pd

# ---- Load data ---- #
General_info = pd.read_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\Clean\General.csv', encoding="utf-8-sig")
Votes_info = pd.read_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\Clean\Voting.csv', encoding="utf-8-sig")


#-------------------------------------- Data preparation ----------------------------------#

# --- Data trasformations ---- #

# -- Categories of tags -- #

## -- General info -- #

# Define all unique tgas
tags = str()
for i in General_info.tags.unique():
    tags = tags + i + ","
    
tags = tags.split(",")

for i in range(0, len(tags)):
    tags[i] = tags[i].strip()

tags2 = list(set(tags))

# get rid of an empty space
del tags2[0]

## gen a dummy per tag 
for tag in tags2:
        General_info[str(tag)] = 0
        General_info.loc[General_info['tags'].str.contains(str(tag)), str(tag)] = 1


# -- Categories of Party Author -- #

## Define unique autor's parties
p_au = str()
for i in General_info.party_autor.unique():
    p_au = p_au + i + ","
    
p_au = p_au.split(",")

for i in range(0, len(p_au)):
    p_au[i] = p_au[i].replace('\'', '').replace('[', '').replace(']', '')
    p_au[i] = p_au[i].strip()

p_au2 = list(set(p_au))

# get rid of an empty space
del p_au2[0]

## gen a dummy per author party 
for party in p_au2:
        key = 'Aut_' + str(party)
        General_info[str(key)] = 0
        General_info.loc[General_info['party_autor'].str.contains(str(party)), str(key)] = 1


# Save daaframe to work on Tableau
General_info.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\For analysis\General_info.csv', encoding="utf-8-sig")

### let's check quickly which are the most commun tags

stat = {'var':[], 'sum':[]}
stats = pd.DataFrame(stat)

## calculate repetitions of tags and save on dataframe
for tag in tags2:
    var_name = tag
    var_sum = General_info[str(tag)].sum()
    stat0 = {'var': tag, 'sum': [var_sum]}
    ds0 = pd.DataFrame(stat0)
    stats = stats.append(ds0)    


# ------------- Votes --------------------- #

## Add new variables that we just created (some varibles will repit, this is only for analysis)
Votes_info = pd.merge(Votes_info, General_info, how='left', on='vote_link')

## save DataFrame
Votes_info.to_csv(r'C:\Users\David\Dropbox\Votaciones_Parlamentarias\For analysis\Votes_info.csv', encoding="utf-8-sig")


#### The rest is carried on in Tableau


