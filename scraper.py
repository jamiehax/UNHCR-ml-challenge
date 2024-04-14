import requests
import os
from bs4 import BeautifulSoup
from typing import Union
import pandas as pd


class Scraper():
    """
    Web Scraper class for FAO FSNAU Early Warning/Early Action in Somalia dashboard.
    
    Scrape
        - `self.scrape` method scrapes data from all URLs in `urls` argument list and 
          saves data to CSV files in 'data/' directory with the type of data as the filename.
    """


    def __init__(self) -> None:
        return


    def scrape(self, urls) -> Union[str, bool]:
        """
        Scrape data from all URLs in urls argument and save each as a CSV with the type of data as the filename.

        Returns:
            - True if all requests were successful.
            - If any URL request fails, exits and returns failed URL request response code.
        """

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

                # save dataframe
                df.to_csv(f'{file_path}.csv', index=False)


            # unsuccessful request
            else:
                return f'Request failed on url: {url}. \n Status code: {response.status_code}'
            
        return True
    

if __name__ == '__main__':

    # example test URLs
    urls = [
        'https://dashboard.fsnau.org/population/arrivals',
        'https://dashboard.fsnau.org/population/departures'
    ]

    scraper = Scraper()
    result = scraper.scrape(urls)
    print(result)
