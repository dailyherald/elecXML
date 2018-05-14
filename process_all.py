import pandas as pd
import numpy as np
import xml.etree.cElementTree as et
print('ready')

tree = et.ElementTree(file="xmlfiles/2018kane.xml")
root = tree.getroot()
print(root.tag, root.attrib)


# Let's get all the contests
dfcols = ['contestID','RaceName','dispOrder']
df_contests = pd.DataFrame(columns=dfcols)

for elem in root.findall(".//County/Election/Contests/"):
    contestID = elem.attrib.get('id')
    RaceName = elem.attrib.get('name')
    dispOrder = elem.attrib.get('displayOrder')
    df_contests = df_contests.append( pd.Series( [contestID, RaceName, dispOrder], index=dfcols) ,ignore_index=True)

df_contests.to_csv('csv/df_contests.csv', index=False, encoding="utf-8")
print('df_contests done')


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

df_choices.to_csv('csv/df_choices.csv', index=False, encoding="utf-8")
print('df_choices done')



# Let's get all the precincts and their splits
prec = ['precID','precname','splitID','splitname']
df_precincts = pd.DataFrame(columns=prec)

for elem in root.findall(".//County/Election/Precincts/"):
    precID = elem.attrib.get('id')
    precname = elem.attrib.get('name')
    for split in elem.findall('./Splits/'):
        splitID = split.attrib.get('id')
        splitname = split.attrib.get('name')
        df_precincts = df_precincts.append( pd.Series( [precID, precname, splitID, splitname], index=prec) ,ignore_index=True)

df_precincts.to_csv('csv/df_precincts.csv', index=False, encoding="utf-8")
print('df_precincts done')


# Let's get all the list of precincts and splits by contest
splitcont = ['contestID','precID','splitID']
df_splitcont = pd.DataFrame(columns=splitcont)

for elem in root.findall(".//County/Election/PrecinctSplitContests/"):
    contestID = elem.attrib.get('contest')
    precID = elem.attrib.get('precinct')
    splitID = elem.attrib.get('split')
    df_splitcont = df_splitcont.append( pd.Series( [contestID, precID, splitID], index=splitcont) ,ignore_index=True)

df_splitcont.to_csv('csv/df_splitcont.csv', index=False, encoding="utf-8")
print('df_splitcont done')


# Let's get vote counts for every contest in every split
tally = ['contestID','choiceID','precID','precname','splitID','splitname','count']
df_tally = pd.DataFrame(columns=tally)

for elem in root.findall(".//County/Election/ElectionTally/"):
    precID = elem.attrib.get('precinct')
    precname = elem.attrib.get('precinctName')
    for split in elem.findall('./SplitTally'):
        splitID = split.attrib.get('split')
        splitname = split.attrib.get('splitName')
        for contest in split.findall('./ContestTally'):
            contestID = contest.attrib.get('contest')
            for choice in contest.findall('./CastVoteTally'):
                choiceID = choice.attrib.get('choice')
                count = choice.attrib.get('count')
                df_tally = df_tally.append( pd.Series( [contestID, choiceID, precID, precname, splitID, splitname, count], index=tally) ,ignore_index=True)

df_tally['cont_ch'] = df_tally['contestID'] + '_' + df_tally['choiceID']

df_tally.to_csv('csv/df_tally.csv', index=False, encoding="utf-8")
print('df_tally done')


# finally, let's make sure the count column is an int,
# then do a pivot table to sum count based on cont_ch
df_sum = df_tally.drop(['contestID','choiceID','precID','precname','splitID','splitname'], axis=1)
df_sum['count'] = (df_sum['count']).astype(int)
df_sum = pd.pivot_table(df_sum, index=['cont_ch'], aggfunc=np.sum)
df_sum.to_csv('csv/df_sum.csv')
print('df_sum done')