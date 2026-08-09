#ELECTRICITY PRICE, USAGE, AND OUTPUT FROM EIA
#NOTE: OPEN SOURCE PROJECT @https://github.com/sguri003/Labor_Stats_Dev
import os
import csv
import requests
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class EIA_Electricity:
    BASE_URL = 'https://api.eia.gov/v2/electricity'

    #CONSTRUCTOR FOR EIA ELECTRICITY PRICE/USAGE/OUTPUT PULL
    def __init__(self, reg_key, out_file_nm, years_back = 10):
        self.reg_key = reg_key
        self.out_file_nm = out_file_nm
        now = datetime.now()
        start = f'{now.year - years_back}-{now.month:02d}'
        end = f'{now.year}-{now.month:02d}'
        price_usage = self.get_price_and_usage(start, end)
        output = self.get_output(start, end)
        self.write_csv(price_usage, output)
        self.plot_trends()

    #retail price (cents/kWh) and usage/sales (million kWh), US total, all sectors
    def get_price_and_usage(self, start, end):
        params = {
            'api_key': self.reg_key,
            'frequency': 'monthly',
            'data[0]': 'price',
            'data[1]': 'sales',
            'facets[sectorid][]': 'ALL',
            'facets[stateid][]': 'US',
            'start': start,
            'end': end,
            'sort[0][column]': 'period',
            'sort[0][direction]': 'asc',
            'length': 5000,
        }
        return self._get(f'{self.BASE_URL}/retail-sales/data/', params)

    #generation/output (thousand MWh), US total, all sectors, all fuel types
    def get_output(self, start, end):
        params = {
            'api_key': self.reg_key,
            'frequency': 'monthly',
            'data[0]': 'generation',
            'facets[fueltypeid][]': 'ALL',
            'facets[location][]': 'US',
            'facets[sectorid][]': '99',
            'start': start,
            'end': end,
            'sort[0][column]': 'period',
            'sort[0][direction]': 'asc',
            'length': 5000,
        }
        return self._get(f'{self.BASE_URL}/electric-power-operational-data/data/', params)

    def _get(self, url, params):
        resp = requests.get(url, params = params)
        if resp.status_code != 200:
            raise RuntimeError(f"EIA API returned {resp.status_code}: {resp.text[:200]}")
        return resp.json()['response']['data']

    #merge price/usage and output by month, write to CSV
    def write_csv(self, price_usage, output):
        if os.path.exists(self.out_file_nm):
            os.remove(self.out_file_nm)
            print(f"File '{self.out_file_nm}' deleted successfully.")
        else:
            print(f"File '{self.out_file_nm}' does not exist.")
        price_by_month = {row['period']: row for row in price_usage}
        output_by_month = {row['period']: row for row in output}
        months = sorted(set(price_by_month) | set(output_by_month))
        with open(self.out_file_nm, mode = 'w', newline = '') as data_file:
            #dt/yr/datekey match the dbo.CPI_Data convention (Dt date, datekey YYYYMMDD int)
            fieldnames = ['Month', 'Price (cents per kWh)', 'Usage (million kWh)', 'Output (thousand MWh)', 'dt', 'yr', 'datekey']
            d_wrtr = csv.writer(data_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
            d_wrtr.writerow(fieldnames)
            for month in months:
                price_row = price_by_month.get(month, {})
                output_row = output_by_month.get(month, {})
                year, mon = month.split('-')
                d_wrtr.writerow([
                    month,
                    price_row.get('price'),
                    price_row.get('sales'),
                    output_row.get('generation'),
                    f'{year}-{mon}-01',
                    int(year),
                    int(f'{year}{mon}01'),
                ])

    #line chart of price, usage, output over time - separate panels since the three
    #metrics are on incompatible scales (cents vs million kWh vs thousand MWh)
    def plot_trends(self):
        df = pd.read_csv(self.out_file_nm)
        df['Month'] = pd.to_datetime(df['Month'], format = '%Y-%m')

        surface = '#fcfcfb'
        panels = [
            ('Price (cents per kWh)', 'Electricity price', '#2a78d6'),
            ('Usage (million kWh)', 'Electricity usage', '#eb6834'),
            ('Output (thousand MWh)', 'Electricity output', '#1baf7a'),
        ]

        last_row = df.iloc[-1]

        sns.set_style('white')
        fig, axes = plt.subplots(3, 1, figsize = (10, 9), sharex = True, facecolor = surface)

        for ax, (column, title, color) in zip(axes, panels):
            ax.set_facecolor(surface)
            sns.lineplot(data = df, x = 'Month', y = column, ax = ax, color = color, linewidth = 2)
            ax.set_title(title, color = '#0b0b0b', fontsize = 11, loc = 'left')
            ax.set_ylabel(column, color = '#52514e', fontsize = 9)
            ax.set_xlabel('')
            ax.grid(True, color = '#e1e0d9', linewidth = 1)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#c3c2b7')
            ax.spines['bottom'].set_color('#c3c2b7')
            ax.tick_params(colors = '#898781', labelsize = 8)

            #direct end-label on the price line - the value at the end, not every point
            if column == 'Price (cents per kWh)':
                ax.set_xlim(right = last_row['Month'] + pd.Timedelta(days = 200))
                ax.annotate(
                    f"{last_row[column]:.2f}¢",
                    xy = (last_row['Month'], last_row[column]),
                    xytext = (6, 0), textcoords = 'offset points',
                    color = '#0b0b0b', fontsize = 9, fontweight = 'bold', va = 'center',
                )

        #quarterly ticks incl. July so summer peaks are directly labeled and comparable
        axes[-1].xaxis.set_major_locator(mdates.MonthLocator(bymonth = [1, 4, 7, 10]))
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        plt.setp(axes[-1].get_xticklabels(), rotation = 45, ha = 'right')

        axes[-1].set_xlabel('Month', color = '#52514e', fontsize = 9)
        fig.suptitle('US Electricity Price, Usage, and Output — Trailing 10 Years', color = '#0b0b0b', fontsize = 13)
        fig.tight_layout(rect = [0, 0, 1, 0.96])
        fig.savefig('Electricity_Trends.png', dpi = 150, facecolor = fig.get_facecolor())
        plt.show()
