import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import plotly.express as px
from plotly.offline import plot  # To plot in Spyder IDE. Opens plots in the default browser
from functools import reduce
url = pd.read_csv("https://raw.githubusercontent.com/openZH/covid_19/master/COVID19_Fallzahlen_CH_total.csv")
covid_confirmed = url['date'], url['abbreviation_canton_and_fl'], url['ncumul_conf']
covid_deaths = url['date'], url['abbreviation_canton_and_fl'], url['ncumul_deceased']
covid_recovered = url['date'], url['abbreviation_canton_and_fl'], url['ncumul_released']

temp = pd.DataFrame(covid_recovered)
covid_recovered = temp.transpose()

temp = pd.DataFrame(covid_confirmed)
covid_confirmed = temp.transpose()

temp = pd.DataFrame(covid_deaths)
covid_deaths = temp.transpose()

covid_confirmed = covid_confirmed.rename(columns={"abbreviation_canton_and_fl": "Canton", 'ncumul_conf': 'Confirmed'})
covid_recovered = covid_recovered.rename(columns={"abbreviation_canton_and_fl": "Canton", 'ncumul_deceased': 'Dead'})
covid_deaths = covid_deaths.rename(columns={"abbreviation_canton_and_fl": "Canton", 'ncumul_released': 'Recovered'})

print('covid confirmed: {}. recovered: {}. died: {}.'.format(covid_confirmed, covid_recovered, covid_deaths))
print(url)

# Handle empty data
covid_confirmed[['Confirmed']] = covid_confirmed[['Confirmed']].fillna('')
covid_confirmed.fillna(0, inplace=True)
covid_deaths[['Dead']] = covid_deaths[['Dead']].fillna('')
covid_deaths.fillna(0, inplace=True)
covid_recovered[['Recovered']] = covid_recovered[['Recovered']].fillna('')
covid_recovered.fillna(0, inplace=True)
