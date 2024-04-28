import os
import pandas as pd


class Aggregator:
    """
    Combine separate CSV files into one aggregated DataFrame using the specified join method.
    """

    def __init__(self, join_method='outer') -> None:
        self.join_method = join_method


    def merge_data(self):
        """
        Merge all data into one DataFrame using specified join method. Return this DataFrame.
        """

        climate_df = self.aggregate_climate()
        print('merged climate data')
        conflict_df = self.aggregate_conflicts()
        df = pd.merge(climate_df, conflict_df, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        print('merged conflict data')

        health_df = self.aggregate_health()
        df = pd.merge(df, health_df, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        print('merged health data')

        malnutrition_df = self.aggregate_malnutrition()
        df = pd.merge(df, malnutrition_df, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        print('merged malnutrition data')

        market_df = self.aggregate_markets()
        df = pd.merge(df, market_df, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        print('merged market data')

        movement_df = self.aggregate_movements()
        df = pd.merge(df, movement_df, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        print('merged movement data')

        return df



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

        # aggregate flood data
        flood_path = 'data/climate/flood'
        flood_dfs = []
        for file_name in os.listdir(flood_path):
            file_path = os.path.join(flood_path, file_name)
            df = self.load_dataframe(file_path, 'River Level')
            flood_dfs.append(df)

        combined_flood = pd.concat(flood_dfs, ignore_index=True)

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
        
        # merge dataframes
        climate_df = pd.merge(climate_df, combined_wp, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        return climate_df
    

    def aggregate_conflicts(self):
        """
        Combine all conflict data into one DataFrame. Return the combined DataFrame.
        """

        # aggregate conflict fatality data
        fatalities_path = 'data/conflicts/fatalities'
        fatalities_dfs = []
        for file_name in os.listdir(fatalities_path):
            file_path = os.path.join(fatalities_path, file_name)
            df = self.load_dataframe(file_path, 'Conflict Fatalities')
            fatalities_dfs.append(df)

        combined_fatality = pd.concat(fatalities_dfs, ignore_index=True)

        # aggregate conflict incident data
        incidents_path = 'data/conflicts/incidents'
        incidents_dfs = []
        for file_name in os.listdir(incidents_path):
            file_path = os.path.join(incidents_path, file_name)
            df = self.load_dataframe(file_path, 'Conflict Incidents')
            incidents_dfs.append(df)

        combined_incidents = pd.concat(incidents_dfs, ignore_index=True)

        # merge dataframes
        conflict_df = pd.merge(combined_fatality, combined_incidents, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        return conflict_df


    def aggregate_health(self):
        """
        Combine all health data into one DataFrame. Return the combined DataFrame.
        """

        # aggregate cholera cases data
        cholera_cases_path = 'data/health/cholera-cases'
        cholera_cases_dfs = []
        for file_name in os.listdir(cholera_cases_path):
            file_path = os.path.join(cholera_cases_path, file_name)
            df = self.load_dataframe(file_path, 'Cholera Cases')
            cholera_cases_dfs.append(df)

        combined_cholera_cases = pd.concat(cholera_cases_dfs, ignore_index=True)

        # aggregate cholera deaths data
        cholera_deaths_path = 'data/health/cholera-deaths'
        cholera_deaths_dfs = []
        for file_name in os.listdir(cholera_deaths_path):
            file_path = os.path.join(cholera_deaths_path, file_name)
            df = self.load_dataframe(file_path, 'Cholera Deaths')
            cholera_deaths_dfs.append(df)

        combined_cholera_deaths = pd.concat(cholera_deaths_dfs, ignore_index=True)

        # merge dataframes
        health_df = pd.merge(combined_cholera_deaths, combined_cholera_cases, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate malaria data
        malaria_path = 'data/health/malaria'
        malaria_dfs = []
        for file_name in os.listdir(malaria_path):
            file_path = os.path.join(malaria_path, file_name)
            df = self.load_dataframe(file_path, 'Malaria')
            malaria_dfs.append(df)

        combined_malaria = pd.concat(malaria_dfs, ignore_index=True)

        # merge dataframes
        health_df = pd.merge(health_df, combined_malaria, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate measles data
        measles_path = 'data/health/measles'
        measles_dfs = []
        for file_name in os.listdir(measles_path):
            file_path = os.path.join(measles_path, file_name)
            df = self.load_dataframe(file_path, 'Measles')
            measles_dfs.append(df)

        combined_measles = pd.concat(measles_dfs, ignore_index=True)

        # merge dataframes
        health_df = pd.merge(health_df, combined_measles, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        return health_df


    def aggregate_malnutrition(self):
        """
        Combine all malnutrition data into one DataFrame. Return the combined DataFrame.
        """

        # aggregate malnutrition data
        malnutrition_path = 'data/malnutrition'
        malnutrition_dfs = []
        for file_name in os.listdir(malnutrition_path):
            file_path = os.path.join(malnutrition_path, file_name)
            df = self.load_dataframe(file_path, 'GAM')
            malnutrition_dfs.append(df)

        combined_malnutrition = pd.concat(malnutrition_dfs, ignore_index=True)
        return combined_malnutrition


    def aggregate_markets(self):
        """
        Combine all market data into one DataFrame. Return the combined DataFrame.
        """

        # aggregate cost of minimum basket data
        cmb_path = 'data/markets/cost-min-basket'
        cmb_dfs = []
        for file_name in os.listdir(cmb_path):
            file_path = os.path.join(cmb_path, file_name)
            df = self.load_dataframe(file_path, 'Cost Min Basket')
            cmb_dfs.append(df)

        combined_cmb = pd.concat(cmb_dfs, ignore_index=True)

        # aggregate goat price data
        goat_path = 'data/markets/goat'
        goat_dfs = []
        for file_name in os.listdir(goat_path):
            file_path = os.path.join(goat_path, file_name)
            df = self.load_dataframe(file_path, 'Goat Price')
            goat_dfs.append(df)

        combined_goat = pd.concat(goat_dfs, ignore_index=True)

        # merge dataframes
        market_df = pd.merge(combined_cmb, combined_goat, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate goat to cereal data
        gtc_path = 'data/markets/goat-to-cereal'
        gtc_dfs = []
        for file_name in os.listdir(gtc_path):
            file_path = os.path.join(gtc_path, file_name)
            df = self.load_dataframe(file_path, 'Goat to Cereal')
            gtc_dfs.append(df)

        combined_gtc = pd.concat(gtc_dfs, ignore_index=True)

        # merge dataframes
        market_df = pd.merge(market_df, combined_gtc, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate maize price data
        maize_path = 'data/markets/maize'
        maize_dfs = []
        for file_name in os.listdir(maize_path):
            file_path = os.path.join(maize_path, file_name)
            df = self.load_dataframe(file_path, 'Maize Price')
            maize_dfs.append(df)

        combined_maize = pd.concat(maize_dfs, ignore_index=True)
        
        # merge dataframes
        market_df = pd.merge(market_df, combined_maize, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate rice price data
        rice_path = 'data/markets/rice'
        rice_dfs = []
        for file_name in os.listdir(rice_path):
            file_path = os.path.join(rice_path, file_name)
            df = self.load_dataframe(file_path, 'Rice Price')
            rice_dfs.append(df)

        combined_rice = pd.concat(rice_dfs, ignore_index=True)

        # merge dataframes
        market_df = pd.merge(market_df, combined_rice, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate sorghum price data
        sorghum_path = 'data/markets/sorghum'
        sorghum_dfs = []
        for file_name in os.listdir(sorghum_path):
            file_path = os.path.join(sorghum_path, file_name)
            df = self.load_dataframe(file_path, 'Sorghum Price')
            sorghum_dfs.append(df)

        combined_sorghum = pd.concat(sorghum_dfs, ignore_index=True)

        # merge dataframes
        market_df = pd.merge(market_df, combined_sorghum, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate wage price data
        wage_path = 'data/markets/wage'
        wage_dfs = []
        for file_name in os.listdir(wage_path):
            file_path = os.path.join(wage_path, file_name)
            df = self.load_dataframe(file_path, 'Wage Price')
            wage_dfs.append(df)

        combined_wage = pd.concat(wage_dfs, ignore_index=True)

        # merge dataframes
        market_df = pd.merge(market_df, combined_wage, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        # aggregate wage to cereal data
        wtc_path = 'data/markets/wage-to-cereal'
        wtc_dfs = []
        for file_name in os.listdir(wtc_path):
            file_path = os.path.join(wtc_path, file_name)
            df = self.load_dataframe(file_path, 'Wage to Cereal')
            wtc_dfs.append(df)

        combined_wtc = pd.concat(wtc_dfs, ignore_index=True)

        # merge dataframes
        market_df = pd.merge(market_df, combined_wtc, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)

        return market_df
    

    def aggregate_movements(self):
        """
        Combine all movement data into one DataFrame. Return the combined DataFrame.
        """

        # aggregate arrival data
        arrivals_path = 'data/movements/arrivals'
        arrivals_dfs = []
        for file_name in os.listdir(arrivals_path):
            file_path = os.path.join(arrivals_path, file_name)
            df = self.load_dataframe(file_path, 'Arrivals')
            arrivals_dfs.append(df)

        combined_arrivals = pd.concat(arrivals_dfs, ignore_index=True)

        # aggregate departure data
        departures_path = 'data/movements/departures'
        departures_dfs = []
        for file_name in os.listdir(departures_path):
            file_path = os.path.join(departures_path, file_name)
            df = self.load_dataframe(file_path, 'Departures')
            departures_dfs.append(df)

        combined_departures = pd.concat(departures_dfs, ignore_index=True)

        # merge dataframes
        movements_df = pd.merge(combined_departures, combined_arrivals, on=['Region', 'District', 'Year', 'Month'], how=self.join_method)
        return movements_df

