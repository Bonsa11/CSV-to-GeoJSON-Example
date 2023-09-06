import geopandas as gpd
import pandas as pd

if __name__ == '__main__':
    # csv downloaded from https://ec.europa.eu/eurostat/databrowser/view/DEMO_R_D3DENS/bookmark/table?lang=en&bookmarkId=ecd9bc29-38c5-4b1d-816f-48e2c860b5b3
    df = pd.read_csv('./data/demo_r_d3dens_linear.csv')

    # turn long table into wide
    df = df.pivot(index='geo', columns='TIME_PERIOD', values='OBS_VALUE')

    # remove countries bby checking length on NUTS ID
    df['length'] = df.index.str.len()
    df = df[df['length'] > 2]

    # get only recent years
    cols = {2018: '2018',
            2019: '2019',
            2020: '2020',
            2021: '2021',
            2022: '2022'}

    # tidying up column names
    df = df[[int(col) for col in cols.keys()]].reset_index()
    cols['geo'] = 'NUTS_ID'
    df = df.rename(columns=cols)

    # saving to CSV for debugging
    df.to_csv('./data/cleaned_data.csv')

    # reading in shape file
    shp_df = gpd.read_file("./geodata/NUTS_RG_20M_2021_4326.shp").to_crs('4326')

    # keeping only level 3 NUTS regions
    shp_df = shp_df.drop(shp_df[shp_df['LEVL_CODE'] != 3].index)

    # merging two dataframes and saving to geojson
    geo_df = pd.merge(shp_df, df, on="NUTS_ID")
    geo_df.to_file('./NUTS_LEVEL_3_POP_Per_KM_2.geojson', driver='GeoJSON')

    # also saving versions w/out UK
    # as central London skews data
    geo_df = geo_df[geo_df["CNTR_CODE"] != "UK"]
    geo_df.to_file('./NUTS_LEVEL_3_POP_Per_KM_2_NO_UK.geojson', driver='GeoJSON')


