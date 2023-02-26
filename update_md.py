'''
更新书籍、游戏、影剧的封面，豆瓣评分等
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path

def get_game_images(keyword, save_path):
    search_url = 'https://www.douban.com/search?cat=3114&q={}'.format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'class': 'result'})
    book_url = items[0].find('a', {'class': 'nbg'})['href']
    book_response = requests.get(book_url, headers=headers)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    rating = book_soup.find('strong').text.strip()
    book_name = book_soup.find('h1').text.strip()
    img_url = book_soup.find('img', {'alt': book_name})['src']
    img_response = requests.get(img_url)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_save_path = os.path.join(save_path, keyword + '_cover.jpg')
    
    return img_save_path, book_url, rating, 'null', img_response

def get_video_images(keyword, save_path):
    search_url = 'https://www.douban.com/search?cat=1002&q={}'.format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'class': 'result'})
    book_url = items[0].find('a', {'class': 'nbg'})['href']
    book_response = requests.get(book_url, headers=headers)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    rating = book_soup.find('strong').text.strip()
    book_name = book_soup.find('h1').text.strip()
    img_url = book_soup.find('img', {'alt': book_name.split('\n')[0]})['src']
    author = book_soup.find('div', {'id': 'info'}).find('a').text.strip()
    img_response = requests.get(img_url)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_save_path = os.path.join(save_path, keyword + '_cover.jpg')
    
    return img_save_path, book_url, rating, author, img_response

def get_book_images(keyword, save_path):
    search_url = 'https://www.douban.com/search?cat=1001&q={}'.format(keyword)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'class': 'result'})
    book_url = items[0].find('a', {'class': 'nbg'})['href']
    book_response = requests.get(book_url, headers=headers)
    book_soup = BeautifulSoup(book_response.text, 'html.parser')
    rating = book_soup.find('strong').text.strip()
    book_name = book_soup.find('h1').text.strip()
    img_url = book_soup.find('img', {'alt': book_name})['src']
    author = book_soup.find('div', {'id': 'info'}).find('a').text.strip()
    img_response = requests.get(img_url)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_save_path = os.path.join(save_path, keyword + '_cover.jpg')
    
    return img_save_path, book_url, rating, author, img_response

def get_files(patterns, path):
    all_files = []
    p = Path(path)
    for item in patterns:
        file_name = p.rglob(f'**/*{item}')
        all_files.extend(file_name)
    return all_files

def update_md(md_data, name, cover_dir, type):
    md_out = md_data.copy()
    try:
        img_path, book_url, rating, author, img_response = globals()['get_' + type + '_images'](name, cover_dir)
    except:
        return md_out
    for idx, line in enumerate(md_data):
        # 更新封面
        if '封面' in line and '!' not in line:
            with open(img_path, 'wb') as f:
                f.write(img_response.content)
            print('\t download cover')
            if os.path.isfile(img_path):
                cover_str = '![[{}]]\n'.format(os.path.basename(img_path))
                md_out[idx] = '封面::' + cover_str + '\n'
            else:
                md_out[idx] = line
        elif 'author' in line:
            if '-' not in md_data[idx+1].split(' '):
                md_out[idx] = line + '  - ' + author + '\n'
        elif 'douban_link' in line and not line.split(':')[-1].strip():
            md_out[idx] = 'douban_link::' + '[豆瓣链接](' + book_url + ')\n'
        elif 'douban_rating' in line and not line.split(':')[-1].strip():
            md_out[idx] = 'douban_rating::' + rating + '\n'

    return md_out

if __name__ == '__main__':
    update_dir = '/Users/rod/OneDrive/Infrod/0-体验清单'
    cover_dir = '/Users/rod/OneDrive/Infrod/附件'
    patterns = ['.md']
    md_files = get_files(patterns, update_dir)
    for md_path in md_files:
        name = os.path.basename(md_path).split('.')[0]
        if name == '体验清单':
            continue
        with open(md_path, "r") as f:
            md_data = f.readlines()
        
        for line in md_data:
            if '类型' in line and '书籍' in line:
                type = 'book'
            elif '类型' in line and '影剧' in line:
                type = 'video'
            elif '类型' in line and '游戏' in line:
                type = 'game'
        md_out = update_md(md_data, name, cover_dir, type)
        if md_data != md_out:
            print('Updating {}...'.format(name))
            with open(md_path,"w") as f:
                f.writelines(md_out)
                

        

    