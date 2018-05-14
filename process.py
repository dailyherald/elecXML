import pandas as pd
import numpy as np
import xml.etree.cElementTree as et
print('ready')

tree = et.ElementTree(file="xmlfiles/2018kane.xml")
root = tree.getroot()
print(root.tag, root.attrib)


# Let's get all the contests

contests = []

for elem in root.findall(".//County/Election/Contests/"):
    contestID = elem.attrib.get('id')
    RaceName = elem.attrib.get('name')
    dispOrder = elem.attrib.get('displayOrder')
    contests.append(( contestID, RaceName, dispOrder ))

df_contests = pd.DataFrame(contests ,columns=['contestID','RaceName','dispOrder'] )
df_contests.to_csv('csv/df_contests.csv', index=False, encoding="utf-8")
print('df_contests done')


# Let's get all the choices
choices = []

for elem in root.findall(".//County/Election/Contests/Contest"):
    contestID = elem.attrib.get('id')
    for ch in elem.findall('./Choice'):
        choiceID = ch.attrib.get('id')
        chtype = ch.attrib.get('type')
        chname = ch.attrib.get('name')
        party = ch.attrib.get('party')
        dispOrder = ch.attrib.get('displayOrder')
        choices.append( ( contestID, choiceID, chtype, chname, party, dispOrder) )

df_choices = pd.DataFrame(choices ,columns=['contestID','choiceID','type','name','party','dispOrder'] )
df_choices['cont_ch'] = df_choices['contestID'] + '_' + df_choices['choiceID']
df_choices.to_csv('csv/df_choices.csv', index=False, encoding="utf-8")
print('df_choices done')

# Let's get vote counts for every contest in every split
# make sure the count column is an int,
# then do a pivot table to sum count based on cont_ch

tally = []

for elem in root.findall(".//County/Election/ElectionTally/PrecinctTally/SplitTally/ContestTally"):
    contestID = elem.attrib.get('contest')
    for choice in elem.findall('./CastVoteTally'):
        choiceID = choice.attrib.get('choice')
        count = choice.attrib.get('count')
        tally.append(( contestID, choiceID, count ))

df_tally = pd.DataFrame(tally ,columns=['contestID', 'choiceID','count'] )
df_tally['cont_ch'] = df_tally['contestID'] + '_' + df_tally['choiceID']

df_tally['count'] = (df_tally['count']).astype(int)
df_tally = pd.pivot_table(df_tally, index=['cont_ch'], aggfunc=np.sum)
df_tally.to_csv('csv/df_sum.csv')
print('df_sum done')