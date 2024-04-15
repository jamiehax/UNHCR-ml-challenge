import requests
import os
from bs4 import BeautifulSoup
from typing import Union
import pandas as pd


class Scraper():
    """
    Web Scraper class for FAO FSNAU Early Warning/Early Action in Somalia dashboard.
    
    Scrape
        - `self.scrape` method scrapes data from all URLs in `urls` argument list.
          
    """


    def __init__(self) -> None:
        return


    def scrape(self, urls: list, to_csv=False) -> Union[str, dict]:
        """
        Scrape data from all URLs in urls argument and return as a dict mapping filenames to DataFrames.

        ARGUMENTS:

        `urls`:
            A list of URLs stored as strings to scrape data from.

        `to_csv`:
            A flag indicating whether to save the DataFrames to CSV files.
            
            If `to_csv` is set to True, saves all scraped pages to separate CSV files in 'data/' directory. The filenames are the part of the URL after '.org'. For example, 'https://dashboard.fsnau.org/population/arrivals' will save to data/population-arrivals.csv.

        
        RETURNS:
            A dict mapping filename to DataFrame for each URL scraped. If any URL fails, exits and returns the status code.
        
        """

        dfs = {}
        for url in urls:

            # get page contents
            response = requests.get(url)

            # successful request - parse data
            if response.status_code == 200:

                # get HTML page content as a string
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

                # make data directory if it doesnt already exist
                output_dir = 'data'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # get filepath from URL
                file_name = url.split('.org/')[-1]
                file_name = file_name.replace('/', '-')
                file_path = os.path.join(output_dir, file_name)

                # save dataframe if `to_csv` is True
                if to_csv:
                    df.to_csv(f'{file_path}.csv', index=False)
                
                # add df to dfs
                dfs[file_name] = df
    
            # unsuccessful request
            else:
                return f'Request failed on url: {url}. \n Status code: {response.status_code}'
            
        return dfs
