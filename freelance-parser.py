import requests
from bs4 import BeautifulSoup as bs

result_file = open('Freelance.txt', 'w', encoding='utf-8')
result_file.write('Заголовок|Цена|Срок выполнения|Ссылка\n')

user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36' +
    '(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

page_counter = 1
while True:
    url = f'https://freelance.ru/project/search?page={page_counter}'
    html = requests.get(url, headers=user_agent).text

    parser = bs(html, 'html.parser')
    
    if parser.find('div', class_='empty') is not None:
        print('\nГотово')
        break
    
    print(f'Страница: {page_counter}', end='\t\t')
    result_file.write(f'\nСтраница #{page_counter}\n')

    tasks = parser.find_all('div', class_='box-shadow')

    for task in tasks:

        if task.find('li', class_='for-business') is not None:
            continue

        title = task.find('h2')
        url = 'https://freelance.ru' + title.find('a')['href']
        title = title['title']

        description = task.find('a', class_='description').text
        price = task.find('div', class_='cost').text
        date = task.find('div', class_='term').text

        task_info = (
            title,
            price,
            date.replace('Срок выполнения: ', ''),
            url
        )

        string = '|'.join(map(str.strip, task_info))

        result_file.write(string + '\n')

    print('OK')

    page_counter += 1

result_file.close()
