import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime

def scrape_rekt_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='post')
    
    rss_items = []
    for article in articles:
        title_element = article.find('h5', class_='post-title').find('a')
        title = title_element.text.strip()
        link = url + title_element['href']
        date = article.find('time').text.strip()
        excerpt = article.find('section', class_='post-excerpt').find('p').text.strip()
        
        rss_item = {
            'title': title,
            'link': link,
            'pubDate': date,
            'description': excerpt
        }
        rss_items.append(rss_item)
    
    return rss_items

def generate_rss_xml(items):
    rss = ET.Element('rss')
    rss.set('version', '2.0')
    
    channel = ET.SubElement(rss, 'channel')
    
    ET.SubElement(channel, 'title').text = 'Rekt News RSS Feed'
    ET.SubElement(channel, 'link').text = 'https://www.rekt.news/'
    ET.SubElement(channel, 'description').text = 'Latest news from Rekt News'
    
    for item in items:
        rss_item = ET.SubElement(channel, 'item')
        ET.SubElement(rss_item, 'title').text = item['title']
        ET.SubElement(rss_item, 'link').text = item['link']
        ET.SubElement(rss_item, 'pubDate').text = item['pubDate']
        ET.SubElement(rss_item, 'description').text = item['description']
    
    rss_str = ET.tostring(rss, encoding='utf-8')
    return rss_str.decode('utf-8')


def save_rss_to_file(xml_str, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(xml_str)
    print(f'RSS feed saved to {filename}')

# Example usage:
if __name__ == '__main__':
    base_url = 'https://www.rekt.news/'
    items = scrape_rekt_news(base_url)
    rss_xml = generate_rss_xml(items)
    save_rss_to_file(rss_xml, './public/rekt_news_rss.xml')
