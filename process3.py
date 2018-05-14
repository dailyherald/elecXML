import pandas as pd
import numpy as np
import xml.etree.cElementTree as et
print('ready')

tree = et.ElementTree(file="xmlfiles/2018kane.xml")
root = tree.getroot()
print(root.tag, root.attrib)


# Let's get all the choices
chcols = ['contestID','choiceID','type','name','party','dispOrder']
df_choices = pd.DataFrame(columns=chcols)

for elem in root.findall(".//County/Election/Contests/Contest"):
    contestID = elem.attrib.get('id')
    for ch in elem.findall('./Choice'):
        choiceID = ch.attrib.get('id')
        chtype = ch.attrib.get('type')
        chname = ch.attrib.get('name')
        dispOrder = ch.attrib.get('displayOrder')
        party = ch.attrib.get('party')
        df_choices = df_choices.append( pd.Series( [contestID, choiceID, chtype, chname, party, dispOrder], index=chcols) ,ignore_index=True)

df_choices['cont_ch'] = df_choices['contestID'] + '_' + df_choices['choiceID']

df_choices.to_csv('csv/df_choices2.csv', index=False, encoding="utf-8")
print('df_choices done')

# Let's get vote counts for every contest in every split
# finally, let's make sure the count column is an int,
# then do a pivot table to sum count based on cont_ch

tally = ['contestID','choiceID','count']
df_tally = pd.DataFrame(columns=tally)

for elem in root.findall(".//County/Election/ElectionTally/PrecinctTally/SplitTally/ContestTally"):
    contestID = elem.attrib.get('contest')
    for choice in elem.findall('./CastVoteTally'):
        choiceID = choice.attrib.get('choice')
        count = choice.attrib.get('count')
        df_tally = df_tally.append( pd.Series( [contestID, choiceID, count], index=tally) ,ignore_index=True)

df_tally['cont_ch'] = df_tally['contestID'] + '_' + df_tally['choiceID']

df_tally['count'] = (df_tally['count']).astype(int)
df_tally = pd.pivot_table(df_tally, index=['cont_ch'], aggfunc=np.sum)
df_tally.to_csv('csv/df_sum3.csv')
print('df_sum done')