import requests
import os
from bs4 import BeautifulSoup
from typing import Union
import pandas as pd


class FSNAUScraper():
    """
    Web Scraper class for FAO FSNAU Early Warning/Early Action in Somalia dashboard.

    Initialize:
        - `start_year`: the year to start scraping data from.
        - `end_year`: the year to stop scraping data from.
        - initialized with base URL to scrape data from. Defaults to FSNAU Dashboard URL.
    
    Scrape single URL:
        - `self.scrape` method scrapes data from single URL passed as argument.

    Scrape Data:
        - `self.scrape_movement` method scrapes data from all population movement pages from `self.start_year` to `self.end_year`. Optionally saves and returns the DataFrames.

        - `self.scrape_market` method scrapes data from all market pages from `self.start_year` to `self.end_year`. Optionally saves and returns the DataFrames.

        - `self.scrape_climate` method scrapes data from all climate pages from `self.start_year` to `self.end_year`. Optionally saves and returns the DataFrames.

        - `self.scrape_nutrition` method scrapes data from all nutrition pages from `self.start_year` to `self.end_year`. Optionally saves and returns the DataFrames.

        - `self.scrape_health` method scrapes data from all health pages from `self.start_year` to `self.end_year`. Optionally saves and returns the DataFrames.

        - `self.scrape_conflicts` method scrapes data from all violent conflict pages from `self.start_year` to `self.end_year`. Optionally saves and returns the DataFrames.
          
    """


    def __init__(self, start_year: int, end_year: int, base_url='https://dashboard.fsnau.org') -> None:
        self.base_url = base_url
        self.start_year = start_year
        self.end_year = end_year


    def scrape(self, url: str, to_csv=False, output_dir=None) -> Union[str, dict]:
        """
        Scrape data from the passed URL and return it as a DataFrame. Optionally save to a CSV file.

        ARGUMENTS:

        `url`:
            A single URL to scrape data from.

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/output_dr' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `output_dir`:
            Directory to save the data to. If passed, subdirectory in 'data' is made, otherwise defaults to 'data' directory.

        RETURNS:
            A DataFrame with the scraped data. If the URL request fails, exits and returns the error.
        
        """

        try:

            # submit URL request and store returned contents as string
            response = requests.get(url)
            html_content = response.text

            # parse HTML string and store in soup object
            soup = BeautifulSoup(html_content, 'html.parser')

            # find all table headers (to become columns)
            data_table = soup.find_all('table')[0]
            headers = [header.text for header in data_table.find_all('th')]
            
            # add datatable rows (to become df rows)
            rows = [row for row in data_table.find_all('tr')]
            row_list = []
            for row in rows:
                row_data = [cell.text.strip() if cell.text.strip() else None for cell in row.find_all('td')]
                row_list.append(row_data)
                
            # create dataframe
            df = pd.DataFrame(row_list, columns=headers)

            # make output data directory if it doesnt already exist
            output_dir = os.path.join('data', output_dir)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # get filepath from URL
            file_name = url.split('.org/')[-1]
            file_name = file_name.replace('/', '-')
            file_path = os.path.join(output_dir, file_name)

            # save dataframe if `to_csv` is True
            if to_csv:
                df.to_csv(f'{file_path}.csv', index=False)

            return df

        # check for any error
        except Exception as e:
            raise e
        

    def scrape_movement(self, to_csv=True, return_dfs=False):
        """
        Scrape data for population movements (arrivals and departures) for all available years. Optionally save to a CSV file and return the DataFrame.

        ARGUMENTS:

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/climate/output_dir' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `return_dfs`:
            If `True` returns the DataFrame as well.

        `return_errors`:
            If `True` returns the errors if any.

        RETURNS:
            Optionally a DataFrame with the scraped data. Always return any error codes from failed scrape attempts.
        
        """

        # base climate data URL
        movement_url = f'{self.base_url}/population'

        # scrape population arrivals data
        arrival_dfs = []
        arrival_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{movement_url}/arrivals/28-Jun-{year}'
            try:
                arrival_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='movements/arrivals'))
            except Exception as e:
                arrival_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{movement_url}/arrivals/28-Dec-{year}'
            try:
                arrival_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='movements/arrivals'))
            except Exception as e:
                arrival_errors.append(e)

        print(f"Scraped population arrival data with {len(arrival_errors)} errors.")

        # scrape population departures data
        departure_dfs = []
        departure_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{movement_url}/departures/28-Jun-{year}'
            try:
                departure_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='movements/departures'))
            except Exception as e:
                departure_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{movement_url}/departures/28-Dec-{year}'
            try:
                departure_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='movements/departures'))
            except Exception as e:
                departure_errors.append(e)

        print(f"Scraped population departure data with {len(departure_errors)} errors.")

        errors = {
            'arrivals': arrival_errors,
            'departures': departure_errors
        }
        
        if return_dfs:
            dfs = {
                'arrivals': arrival_dfs,
                'departures': departure_dfs
            }
            return dfs, errors
        else:
            return errors


    def scrape_market(self, to_csv=True, return_dfs=False):
        """
        Scrape data for market prices (maize, sorghum, rice, goat, wage,) for 2015 onwards. Optionally save to a CSV file and return the DataFrame.

        ARGUMENTS:

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/climate/output_dir' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `return_dfs`:
            If `True` returns the DataFrame as well.

        `return_errors`:
            If `True` returns the errors if any.

        RETURNS:
            Optionally a DataFrame with the scraped data. Always return any error codes from failed scrape attempts.
        
        """
        
        # base climate data URL
        market_url = f'{self.base_url}/markets'

        # TODO: write scraping code


    def scrape_climate(self, to_csv=True, return_dfs=False):
        """
        Scrape data from all climate related pages for 2015 onwards. Optionally save to a CSV file and return the DataFrame.

        ARGUMENTS:

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/climate/output_dir' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `return_dfs`:
            If `True` returns the DataFrame as well.

        `return_errors`:
            If `True` returns the errors if any.

        RETURNS:
            Optionally a DataFrame with the scraped data. Always return any error codes from failed scrape attempts.
        
        """

        # base climate data URL
        climate_url = f'{self.base_url}/climate'

        # scrape combined drought index (CDI) data
        cdi_dfs = []
        cdi_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{climate_url}/cdi/28-Jun-{year}'
            try:
                cdi_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='climate/cdi'))
            except Exception as e:
                cdi_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{climate_url}/cdi/28-Dec-{year}'
            try:
                cdi_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='climate/cdi'))
            except Exception as e:
                cdi_errors.append(e)

        print(f"Scraped CDI (drought) data with {len(cdi_errors)} errors.")


        # scrape vegetation cover index (NDVI) data
        ndvi_dfs = []
        ndvi_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{climate_url}/ndvi/28-Jun-{year}'
            try:
                ndvi_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='climate/ndvi'))
            except Exception as e:
                ndvi_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{climate_url}/ndvi/28-Dec-{year}'
            try:
                ndvi_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='climate/ndvi'))
            except Exception as e:
               ndvi_errors.append(e)

        print(f"Scraped NDVI (vegetation) data with {len(ndvi_errors)} errors.")


        # scrape flood data
        flood_dfs = []
        flood_errors = []
        for year in range(self.start_year, 2021, 1): # flood data stops at 2021

            # try to scrape first half of year
            first_half = f'{climate_url}/river-levels/28-Jun-{year}'
            try:
               flood_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='climate/flood'))
            except Exception as e:
                flood_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{climate_url}/river-levels/28-Dec-{year}'
            try:
                flood_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='climate/flood'))
            except Exception as e:
                flood_errors.append(e)

        print(f"Scraped Flood data with {len(flood_errors)} errors.")


        # scrape rainfall data
        rainfall_dfs = []
        rainfall_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{climate_url}/rainfall/28-Jun-{year}'
            try:
               rainfall_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='climate/rainfall'))
            except Exception as e:
                rainfall_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{climate_url}/rainfall/28-Dec-{year}'
            try:
                rainfall_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='climate/rainfall'))
            except Exception as e:
                rainfall_errors.append(e)

        print(f"Scraped Rainfall data with {len(rainfall_errors)} errors.")


        # scrape water price (wp) data
        wp_dfs = []
        wp_errors = []
        for year in range(self.start_year, self.end_year, 1):
    
            # try to scrape first half of year
            first_half = f'{climate_url}/price-of-water/28-Jun-{year}'
            try:
               wp_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='climate/water-price'))
            except Exception as e:
                wp_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{climate_url}/price-of-water/28-Dec-{year}'
            try:
                wp_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='climate/water-price'))
            except Exception as e:
                wp_errors.append(e)

        print(f"Scraped Water Price data with {len(wp_errors)} errors.")

        errors = {
            'cdi': cdi_errors,
            'ndvi': ndvi_errors,
            'flood': flood_errors,
            'rainfall': rainfall_errors,
            'wp': wp_errors
        }
        
        if return_dfs:
            dfs = {
                'cdi': cdi_dfs,
                'ndvi': ndvi_dfs,
                'flood': flood_dfs,
                'rainfall': rainfall_dfs,
                'wp': wp_dfs
            }
            
            return dfs, errors
        else:
            return errors
        

    def scrape_nutrition(self, to_csv=True, return_dfs=False):
        """
        Scrape data for malnutrition for 2016 onwards. Optionally save to a CSV file and return the DataFrame.

        ARGUMENTS:

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/climate/output_dir' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `return_dfs`:
            If `True` returns the DataFrame as well.

        `return_errors`:
            If `True` returns the errors if any.

        RETURNS:
            Optionally a DataFrame with the scraped data. Always return any error codes from failed scrape attempts.
        
        """

        # base climate data URL
        nutrition_url = f'{self.base_url}/nutrition/gam'

        # scrape malnutrition data
        nutrition_dfs = []
        nutrition_errors = []
        for year in range(self.start_year + 1, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{nutrition_url}/28-Jun-{year}'
            try:
                nutrition_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='malnutrition'))
            except Exception as e:
                nutrition_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{nutrition_url}/28-Dec-{year}'
            try:
                nutrition_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='malnutrition'))
            except Exception as e:
                nutrition_errors.append(e)

        print(f"Scraped malnutrition data with {len(nutrition_errors)} errors.")

        errors = {
            'malnutrition': nutrition_errors,
        }
        
        if return_dfs:
            dfs = {
                'malnutrition': nutrition_dfs,
            }
            return dfs, errors
        else:
            return errors


    def scrape_health(self, to_csv=True, return_dfs=False):
        """
        Scrape data for health issues (cholera, measles, malaria) for 2015 onwards. Optionally save to a CSV file and return the DataFrame.

        ARGUMENTS:

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/climate/output_dir' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `return_dfs`:
            If `True` returns the DataFrame as well.

        `return_errors`:
            If `True` returns the errors if any.

        RETURNS:
            Optionally a DataFrame with the scraped data. Always return any error codes from failed scrape attempts.
        
        """

        # base climate data URL
        health_url = f'{self.base_url}/health'

        # scrape cholera cases data
        cholera_cases_dfs = []
        cholera_cases_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{health_url}/awd/28-Jun-{year}'
            try:
                cholera_cases_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='health/cholera-cases'))
            except Exception as e:
                cholera_cases_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{health_url}/awd/28-Dec-{year}'
            try:
                cholera_cases_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='health/cholera-cases'))
            except Exception as e:
                cholera_cases_errors.append(e)

        print(f"Scraped cholera cases data with {len(cholera_cases_errors)} errors.")

        # scrape cholera deaths data
        cholera_deaths_dfs = []
        cholera_deaths_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{health_url}/awd-deaths/28-Jun-{year}'
            try:
                cholera_deaths_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='health/cholera-deaths'))
            except Exception as e:
                cholera_deaths_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{health_url}/awd-deaths/28-Dec-{year}'
            try:
                cholera_deaths_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='health/cholera-deaths'))
            except Exception as e:
                cholera_deaths_errors.append(e)

        print(f"Scraped cholera death data with {len(cholera_deaths_errors)} errors.")

        # scrape measles cases data
        measles_dfs = []
        measles_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{health_url}/measles/28-Jun-{year}'
            try:
                measles_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='health/measles'))
            except Exception as e:
                measles_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{health_url}/measles/28-Dec-{year}'
            try:
                measles_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='health/measles'))
            except Exception as e:
                measles_errors.append(e)

        print(f"Scraped measles cases data with {len(measles_errors)} errors.")

        # scrape malaria cases data
        malaria_dfs = []
        malaria_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{health_url}/malaria/28-Jun-{year}'
            try:
                malaria_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='health/malaria'))
            except Exception as e:
                malaria_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{health_url}/malaria/28-Dec-{year}'
            try:
                malaria_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='health/malaria'))
            except Exception as e:
                malaria_errors.append(e)

        print(f"Scraped malaria cases data with {len(malaria_errors)} errors.")


        errors = {
            'cholera_cases': cholera_cases_errors,
            'cholera_deaths': cholera_deaths_errors,
            'measles': measles_errors,
            'malaria': malaria_errors
        }
        
        if return_dfs:
            dfs = {
                'cholera_cases': cholera_cases_dfs,
            'cholera_deaths': cholera_deaths_dfs,
            'measles': measles_dfs,
            'malaria': malaria_dfs
            }
            return dfs, errors
        else:
            return errors


    def scrape_conflicts(self, to_csv=True, return_dfs=False):
        """
        Scrape data for violent conflicts (incidents and fatalities) for 2015 onwards. Optionally save to a CSV file and return the DataFrame.

        ARGUMENTS:

        `to_csv`:
            A flag indicating whether to save the DataFrame to a CSV file.
            
            If `to_csv` is set to True, saves scraped data to a CSV file in 'data/climate/output_dir' directory. The filename is the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        `return_dfs`:
            If `True` returns the DataFrame as well.

        `return_errors`:
            If `True` returns the errors if any.

        RETURNS:
            Optionally a DataFrame with the scraped data. Always return any error codes from failed scrape attempts.
        
        """

        # base climate data URL
        conflicts_url = f'{self.base_url}/insecurity'

        # scrape violent conflict incident data
        incidents_dfs = []
        incidents_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{conflicts_url}/incidents/28-Jun-{year}'
            try:
                incidents_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='conflicts/incidents'))
            except Exception as e:
                incidents_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{conflicts_url}/incidents/28-Dec-{year}'
            try:
                incidents_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='conflicts/fatalitites'))
            except Exception as e:
                incidents_errors.append(e)

        print(f"Scraped conflict incident data with {len(incidents_errors)} errors.")

        # scrape violent conflict fatality data
        fatalities_dfs = []
        fatalities_errors = []
        for year in range(self.start_year, self.end_year, 1):

            # try to scrape first half of year
            first_half = f'{conflicts_url}/fatalities/28-Jun-{year}'
            try:
                fatalities_dfs.append(self.scrape(first_half, to_csv=to_csv, output_dir='conflicts/fatalities'))
            except Exception as e:
                fatalities_errors.append(e)
            
            # try to scrape second half of year
            second_half = f'{conflicts_url}/fatalities/28-Dec-{year}'
            try:
                fatalities_dfs.append(self.scrape(second_half, to_csv=to_csv, output_dir='conflicts/fatalitites'))
            except Exception as e:
                fatalities_errors.append(e)

        print(f"Scraped conflict fatality data with {len(fatalities_errors)} errors.")

        errors = {
            'incident': incidents_errors,
            'fatality': fatalities_errors
        }
        
        if return_dfs:
            dfs = {
                'incidents': incidents_dfs,
                'fatalities': fatalities_dfs
            }
            return dfs, errors
        else:
            return errors
