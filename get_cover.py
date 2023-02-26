import requests
from bs4 import BeautifulSoup
import os

def get_book_images(keyword, save_path):
    search_url = 'https://www.douban.com/subject_search?search_text={}&cat=1001'.format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'class': 'result'})
    # for item in items:
    book_url = items[0].find('a', {'class': 'nbg'})['href']
    book_response = requests.get(book_url, headers=headers)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    book_name = book_soup.find('h1').text.strip()
    img_url = book_soup.find('img', {'alt': book_name})['src']
    img_response = requests.get(img_url)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_save_path = os.path.join(save_path, book_name + '_cover.jpg')
    with open(img_save_path, 'wb') as f:
        f.write(img_response.content)
    return img_save_path

if __name__ == '__main__':
    keyword = "蛙"
    save_path = "/Users/rod/OneDrive/Infrod/附件"
    get_book_images(keyword, save_path)
