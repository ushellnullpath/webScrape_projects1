'''
Project: webScrape_projects1
By: ushellnullpath
Description:
A web scraping project to gather comprehensive data on the 
top 50 anime series as ranked on IMDB.
Different libraries that have been used are beautifulsoup, requests,
and pandas.
Last updated on (D/M/Y): 27/10/2023
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd


class TopAnimeScraper:
    def __init__(self, url):
        self.url = url

    def scrape_and_save(self, output_file="data/top50_anime_series_tier.csv"):
        try:
            # sending a GET request to the first page's URL
            source = requests.get(self.url)
            source.raise_for_status()

            # parsing the HTML content of the page
            soup = BeautifulSoup(source.text, 'html.parser')

            # finding the list of top 50 anime series
            top_50 = soup.find(
                "div", class_="lister-list").find_all("div", class_="lister-item mode-simple")

            tier_list = []

            for anime in top_50:
                # extracting relevant information from the HTML
                rank = anime.find(
                    "div", class_="col-title").get_text(strip=True).split(".")[0]
                title = anime.find("div", class_="col-title").a.text
                year = anime.find(
                    "span", class_="lister-item-year text-muted unbold").text
                rating = anime.find(
                    "div", class_="col-imdb-rating").strong.text.strip()

                # appending the extracted data to the tier_list
                tier_list.append([rank, title, year, rating])

            # creating a DataFrame from the collected data
            df = pd.DataFrame(tier_list, columns=[
                              "ANIME_RANK", "ANIME_TITLE", "YEAR", "IMDB_RATING"])
            df.set_index("ANIME_RANK", inplace=True)

            # saving the DataFrame to a CSV file with UTF-8 encoding
            df.to_csv(output_file, encoding="utf-8-sig")
            print(f"Data has been saved to: {output_file}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    url = "https://www.imdb.com/search/title/?title_type=tv_series&num_votes=1000,&genres=animation&keywords=anime&view=simple"
    scraper = TopAnimeScraper(url)
    scraper.scrape_and_save()
