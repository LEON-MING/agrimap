import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.figure as figure
import matplotlib.patches as mpatches
import base64
from io import BytesIO
from functools import lru_cache

def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords'
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

def calc_color(data, color=None):
    if color == 1:
        color_sq = ['#dadaebFF','#bcbddcF0','#9e9ac8F0', '#807dbaF0','#6a51a3F0','#54278fF0']
        colors = 'Purples'
    elif color == 2:
        color_sq = ['#c7e9b4','#7fcdbb','#41b6c4', '#1d91c0','#225ea8','#253494']
        colors = 'YlGnBu'
    elif color == 3:
        color_sq = ['#f7f7f7','#d9d9d9','#bdbdbd', '#969696','#636363','#252525']
        colors = 'Greys'
    elif color == 9:
        color_sq = ['#ff0000','#ff0000','#ff0000', '#ff0000','#ff0000','#ff0000']
    else:
        color_sq = ['#ffffd4','#fee391','#fec44f', '#fe9929','#d95f0e','#993404']
        colors = 'YlOrBr'
    color_nums, bins = pd.qcut(data, 6, retbins=True, labels=list(range(6)))
    color_codes = [color_sq[num] for num in color_nums]

    return color_sq, color_codes, bins

def plot_map_fill_multiples_ids_tone(sf, title, counties,
                                     print_id, color_codes,
                                     color_sq, bins,
                                     figsize):
    fig = figure.Figure(figsize = figsize)
    ax = fig.subplots()
    fig.suptitle(title, fontsize=16, y=0.85)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    patches = []
    for i in range(len(color_sq)):
        patches.append(mpatches.Patch(color=color_sq[i],
            label=("[" + str(round(bins[i], 3)) + ", " + str(round(bins[i+1], 3)) + ")")))
    ax.legend(handles=patches)

    # Plot selected counties
    for id in counties:
        shape_ex = sf.shape(id)
        x_lon = np.empty(len(shape_ex.points))
        y_lat = np.empty(len(shape_ex.points))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        ax.fill(x_lon, y_lat, color_codes[counties.index(id)])
        if print_id:
            x0 = np.mean(x_lon)
            y0 = np.mean(y_lat)
            ax.text(x0, y0, id, fontsize=10)

    return fig

def plot_data(sf, title, county_ids, data=None, color=None, print_id=False, figsize=(15, 9)):
    '''
    Plot map with selected comunes, using specific color
    '''

    color_sq, color_codes, bins = calc_color(data, color)
    df = read_shapefile(sf)
    return plot_map_fill_multiples_ids_tone(sf, title, county_ids, print_id,
        color_codes, color_sq, bins, figsize)

# Load files and dataframes
sf = shp.Reader("./data/cntymap/cntymap.shp", encoding='latin1')
counties_df = read_shapefile(sf)
rainfall_df = pd.read_csv("./data/pptAprOct.csv")
temp_df = pd.read_csv("./data/gddAprOctAvg.csv")
# Change stco type to int
counties_df.stco = counties_df.stco.astype(int)
counties_df = counties_df.drop(['SP_ID', 'SP_ID_1', 'atlas_caps', 'atlas_area', 'entity', 'cntya', 'cntyn', 'fid', 'eastm100',
                 'coords', 'atlas_acre', 'atlas_stco'], axis=1)

# Get california county ids
california_counties = counties_df[(counties_df['stco'].astype(int) < 7000) & (counties_df['stco'].astype(int) >= 6000)]
california_county_ids = list(california_counties.index)

rainfall_maps = {}
def get_rainfall_map(year):
    if year not in rainfall_maps:
        california_rainfall = rainfall_df.loc[rainfall_df['stco'].isin(california_counties.stco) & (rainfall_df['year'] == year)]
        california_rainfall = california_counties.merge(california_rainfall, how='left', on='stco')
        california_rainfall = california_rainfall.fillna(california_rainfall.mean()).ppt

        fig = plot_data(sf, 'California Rainfall ' + str(year), california_county_ids, data=california_rainfall, color=1, print_id=False, figsize=(8,11))
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        rainfall_maps[year] = f"data:image/png;base64,{data}"
    return rainfall_maps[year]

temp_maps = {}
def get_temp_map(year):
    if year not in temp_maps:
        california_temp = temp_df.loc[temp_df['stco'].isin(california_counties.stco) & (temp_df['year'] == year)]
        california_temp = california_counties.merge(california_temp, how='left', on='stco')
        california_temp = california_temp.fillna(california_temp.mean()).avg_temp

        fig = plot_data(sf, 'California Temp ' + str(year), california_county_ids, data=california_temp, color=1, print_id=False, figsize=(8,11))
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        temp_maps[year] = f"data:image/png;base64,{data}"
    return temp_maps[year]
