import pandas as pd
import gmaps
from IPython.display import display

data = pd.read_csv("data.csv")
df = pd.DataFrame(data)
df.head()
print(df.shape)

mylist = ["5/27/20"]
df2 = df[df[mylist].ne(0).all(1)]
print(df2)
gmaps.configure(api_key="")
locations = df2[['Lat', 'Long']]
weights = df2["5/27/20"]
fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations, weights=weights, max_intensity=100, point_radius=20.0))
fig
