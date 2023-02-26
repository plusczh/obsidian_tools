'''
excel图书库转为obsidian md格式
'''
import pandas as pd
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
    excel_path = '/Users/rod/Downloads/体验清单.xlsx'
    save_dir = '/Users/rod/OneDrive/Infrod/0-体验清单'
    cover_dir = '/Users/rod/OneDrive/Infrod/附件'
    df = pd.read_excel("/Users/rod/Downloads/体验清单.xlsx", sheet_name='书籍')
    with open("/Users/rod/OneDrive/Infrod/模板/书籍模板.md", "r") as f:
        templater = f.readlines()
    star_emoji_map = {'1.0': '★', '2.0': '★★', '3.0': '★★★', '4.0': '★★★★', '5.0': '★★★★★',
                      '1.5': '★☆', '2.5': '★★☆', '3.5': '★★★☆', '4.5': '★★★★☆'}
    for index, row in df.iterrows():
        # print(row)
        name = str(row['名称'])
        print('Processing {}.....'.format(name))
        new_lines = []
        for line in templater:
            if 'author' in line:
                new_line = line + '  - ' + row['作者'] + '\n'
            elif '完成:' in line:
                new_line = '完成: true\n'
            elif '完成时间' in line:
                time_str = '-'.join(row['完成时间'].split('/'))
                new_line = line.strip() + ' ' + time_str + '\n'
            elif '时长' in line:
                new_line = '时长: 5\n'
            elif '评分' in line:
                star_str = star_emoji_map[str(row['评分'])]
                new_line = line.strip() + ' ' + star_str + '\n'
            elif 'tags' in line:
                new_line = line + '  - ' + row['标签'] + '\n'
            elif '封面' in line:
                try:
                    img_path = get_book_images(name, cover_dir)
                    print('\t download cover')
                except:
                    # 无法下载图片时
                    img_path = os.path.join(cover_dir, name + '_cover.jpg')
                if os.path.isfile(img_path):
                    cover_str = '![[{}]]\n'.format(os.path.basename(img_path))
                    new_line = line.strip() + cover_str + '\n'
                else:
                    new_line = line
            else:
                new_line = line
            new_lines.append(new_line)
        if not row.isnull()['评论']:
            new_lines.append(str(row['评论']) + '\n')
        md_save_path = os.path.join(save_dir, name + '.md')
        with open(md_save_path,"w") as f:
            f.writelines(new_lines)

        
