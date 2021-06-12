from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def scraper():    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_soup = soup.find_all('section', class_='image_and_description_container')
    nr = news_soup[0].find('div',class_='col-md-8')
    news ={'title':nr.find_all('div',class_='content_title')[0].text,
      'p':nr.find_all('div',class_='article_teaser_body')[0].text}
    
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    header_soup = soup.find('div', class_='header')
    featured_image_url = url+header_soup.find('img',class_='headerimage')['src']
    
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[0]
    table_data = df.values.tolist()

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []
    for i in soup.find_all('div', class_='item'):
        href = i.find('a')['href']
        browser.visit(url+href)
        html_l2 = browser.html
        soup_l2 = BeautifulSoup(html_l2, 'html.parser')
        cover_soup = soup_l2.find('div',class_='cover')
        h2 = cover_soup.find('h2',class_='title').text
        dw_soup = soup_l2.find('div',class_='downloads')
        a  = dw_soup.find('a')['href']
        hemisphere_image_urls.append({'Title':' '.join(h2.split(' ')[:-1]),\
            'Src':url+a})

    data = {
        'News': news,
        'Feature_img': featured_image_url,
        'table': table_data,
        'hemisphere_img':hemisphere_image_urls
    }
    return data
if __name__ == '__main__':
    print(scraper())