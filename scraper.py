import requests
import os
from bs4 import BeautifulSoup
from typing import Union
import pandas as pd


class Scraper():
    """
    Web Scraper class for FAO FSNAU Early Warning/Early Action in Somalia dashboard.

    Initialize:
        - initialized with base URL to scrape data from. Defaults to FSNAU Dashboard URL.
    
    Scrape single URL:
        - `self.scrape` method scrapes data from single URL passed as argument.

    Scrape Climate Data:
        - `self.scrape_climate` method scrapes data from all climate pages for all available years. Optionally saves and returns the DataFrames.
          
    """


    def __init__(self, base_url='https://dashboard.fsnau.org') -> None:
        self.base_url = base_url


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

        # check for error in HTML request
        except requests.exceptions.RequestException as e:
            raise Exception(f'Request failed on url: {url}. \n Error: {e}')
        


    def scrape_climate(self, to_csv=True, return_dfs=True):
        """
        Scrape data from all Climate related pages for all available years. Optionally save to a CSV file and return the DataFrame.

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
        for year in range(2015, 2024, 1):

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
        for year in range(2008, 2024, 1):

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
        for year in range(2000, 2022, 1):

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
        for year in range(2000, 2024, 1):

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
        for year in range(2011, 2024, 1):
    
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

        dfs = {
            'cdi': cdi_dfs,
            'ndvi': ndvi_dfs,
            'flood': flood_dfs,
            'rainfall': rainfall_dfs,
            'wp': wp_dfs
        }

        errors = {
            'cdi': cdi_errors,
            'ndvi': ndvi_errors,
            'flood': flood_errors,
            'rainfall': rainfall_errors,
            'wp': wp_errors
        }
        
        if return_dfs:
            return dfs, errors
        else:
            return errors