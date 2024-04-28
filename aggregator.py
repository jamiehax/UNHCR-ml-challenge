import os
import pandas as pd


class Aggregator:
    """
    Combine separate CSV files into one aggregated DataFrame using the specified join method.
    """

    def __init__(self, join_method='outer') -> None:
        self.join_method = join_method


    def load_dataframe(self, df_path, value_name):
        """
        Read in and return a DataFrame for the CSV file passed as df_path. 
            - Drop the first row (which seems to always be NaNs)
            - Converts the DataFrame to long format by adding a column for the data values passed in value_name arg
        """

        df = pd.read_csv(df_path)

        # drop first row (which is all NA values)
        df.drop(labels=0, axis='index', inplace=True)

        # drop extra label column
        df.drop(labels='#', axis='columns', inplace=True)

        # convert data to long format
        df_long = pd.melt(df, id_vars=['Region', 'District'], var_name='Date', value_name=value_name)

        # split date into Month and Year columns
        df_long[['Month', 'Year']] = df_long['Date'].str.split('-', expand=True)
        df_long.drop(labels='Date', axis='columns', inplace=True)

        # change column data types
        df_long['Year'] = pd.to_numeric(df_long['Year'])
        df_long['Month'] = df_long['Month'].astype('category')
        df_long['Region'] = df_long['Region'].astype('category')
        df_long['District'] = df_long['District'].astype('category')

        return df_long


    def aggregate_climate(self):
        """
        Combine all climate data into one DataFrame. Return the combined DataFrame.
        """

        # aggregate cdi data
        cdi_path = 'data/climate/cdi'
        cdi_dfs = []
        for file_name in os.listdir(cdi_path):
            file_path = os.path.join(cdi_path, file_name)
            df = self.load_dataframe(file_path, 'CDI')
            cdi_dfs.append(df)

        combined_cdi = pd.concat(cdi_dfs, ignore_index=True)
        print('Combined CDI CSVs')

        # aggregate flood data
        flood_path = 'data/climate/flood'
        flood_dfs = []
        for file_name in os.listdir(flood_path):
            file_path = os.path.join(flood_path, file_name)
            df = self.load_dataframe(file_path, 'River Level')
            flood_dfs.append(df)

        combined_flood = pd.concat(flood_dfs, ignore_index=True)
        print('Combined flood CSVs')

        # merge dataframes
        climate_df = pd.merge(combined_cdi, combined_flood, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate ndvi data
        ndvi_path = 'data/climate/ndvi'
        ndvi_dfs = []
        for file_name in os.listdir(ndvi_path):
            file_path = os.path.join(ndvi_path, file_name)
            df = self.load_dataframe(file_path, 'NDVI')
            ndvi_dfs.append(df)

        combined_ndvi = pd.concat(ndvi_dfs, ignore_index=True)
        print('Combined NDVI CSVs')

        # merge dataframes
        climate_df = pd.merge(climate_df, combined_ndvi, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate rainfall data
        rainfall_path = 'data/climate/rainfall'
        rainfall_dfs = []
        for file_name in os.listdir(rainfall_path):
            file_path = os.path.join(rainfall_path, file_name)
            df = self.load_dataframe(file_path, 'Rainfall')
            rainfall_dfs.append(df)

        combined_rainfall = pd.concat(rainfall_dfs, ignore_index=True)
        print('Combined rainfall CSVs')

        # merge dataframes
        climate_df = pd.merge(climate_df, combined_rainfall, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate water price data
        wp_path = 'data/climate/water-price'
        wp_dfs = []
        for file_name in os.listdir(wp_path):
            file_path = os.path.join(wp_path, file_name)
            df = self.load_dataframe(file_path, 'Water Price')
            wp_dfs.append(df)

        combined_wp = pd.concat(wp_dfs, ignore_index=True)
        print('Combined water price CSVs')
        
        # merge dataframes
        climate_df = pd.merge(climate_df, combined_wp, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        return climate_df