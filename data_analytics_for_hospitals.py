import pandas as pd
import matplotlib.pyplot as plt
general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sports = pd.read_csv('test/sports.csv')
prenatal.columns = general.columns
sports.columns = general.columns
sports.dropna(how='all',inplace=True)
frames = [general, prenatal, sports]

df = pd.concat(frames)
df.drop('Unnamed: 0', axis=1, inplace=True)
df.dropna(how='all',inplace=True)
df.gender.fillna('f', inplace=True)
def f(gender):
    if gender == 'man' or gender == 'male':
        return 'm'
    elif gender == 'female' or gender == 'woman':
        return 'f'
df.gender = df.gender.apply(f)
df.fillna(0, inplace=True)
plt.hist(df.hospital)
ans1 = df['hospital'].value_counts().sort_values(ascending=False).index[0]
diag = df.groupby('diagnosis').agg({'hospital': 'count'})
plt.pie(diag.values.flatten(), labels=diag.index)
plt.show()
ans2 = 318 / df.shape[0]
df.groupby('diagnosis').agg({'hospital': 'count'}).sort_values(['hospital'], ascending=False)
print(f'The answer to the 1st question: {ans1}')
print('The answer to the 2nd question: sprain')
print(f'The answer to the 3d question: It\'s because...')
'''4-th part'''
# ans1 = df['hospital'].value_counts().sort_values(ascending=False).index[0]
# n_general = general.shape[0]
# n_sports = df.query('hospital == "sports"').hospital.value_counts()
#
# ans2 = general.query('diagnosis=="stomach"').diagnosis.value_counts()/n_general
# ans3 = df.query('hospital == "sports" & diagnosis=="dislocation"').diagnosis.value_counts()/(n_sports[0])
# general_med = general.age.median()
# sports_med = sports.age.median()
# ans4 = general_med - sports_med
# print(f'The answer to the 1st question is {ans1}')
# print(f'The answer to the 2nd question is {round(ans2[0],3)}')
# print(f'The answer to the 3d question is {round(ans3[0], 3)}')
# print(f'The answer to the 4th question is {ans4}')
