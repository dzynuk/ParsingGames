import requests
from bs4 import BeautifulSoup
import csv

url = 'https://store.steampowered.com/search/results/'
count = 100
start = 0

links = []

while start < 2000:
    params = {
        'query': '',
        'start': str(start),
        'count': '100',
        'dynamic_data': '',
        'sort_by': '_ASC',
        'snr': '1_7_7_240_7',
        'tags': '1676',
        'category1': '998',
        'supportedlang': 'english'
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    for game in soup.find_all('a', {'class': 'search_result_row'}):
        review_summary = game.find('span', {'class': 'search_review_summary'})
        if review_summary and review_summary.has_attr('class'):
            review_class = review_summary['class'][1]
            if review_class in ['very_positive', 'overwhelmingly_positive', 'mixed', 'mostly_positive', 'positive']:
                game_link = game['href']
                links.append(game_link)

    start += count

with open('allgames.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Game Name', 'Game Link', 'Developer Name', 'Publisher Name', 'Game Genre', 'Platform',
                     'Style Genre',
                     'Release Date', 'Price', 'Rating', 'Positive Review', 'Review'])
    for other_game in links:
        try:
            response = requests.get(other_game)
            soup = BeautifulSoup(response.text, 'html.parser')
            game_div = soup.find('div', {'class': 'glance_ctn'})
            style_genre = []
            game_name = soup.find('div', {'id': 'appHubAppName'}).text.strip()
            developers_list = game_div.find('div', {'id': 'developers_list'}).find_all('a')
            developer_name = [dev.text.strip() for dev in developers_list]
            publisher_list = game_div.find('div', {'class': 'dev_row'}).find_all('a')
            publisher_name = [dev.text.strip() for dev in publisher_list]
            game_genre = ','.join([a.text.strip() for a in game_div.find('div', {'class': 'glance_tags popular_tags'}).find_all('a')])
            genre = ['2.5D', '2D', '360 Video', '3D', 'Abstract', 'Anime', 'Cartoon', 'Cartoony', 'Cinematic',
                     'Colorful', 'Comic Book', 'Cute', 'First-Person', 'FMV', 'Hand-drawn', 'Isometric', 'Minimalist',
                     'Noir', 'Pixel Graphics', 'Psychedelic', 'Realistic', 'Split Screen', 'Stylized', 'Text-Based',
                     'Third Person', 'Top-Down', 'Voxel', 'VR']
            for x in game_genre.split(','):
                if x in genre:
                    style_genre.append(x)
            platform_spans = soup.find_all('span', {'class': 'platform_img'})
            platforms = set(span['class'][1] for span in platform_spans)
            release_date = game_div.find('div', {'class': 'date'}).text.strip()

            game_div_price = soup.find('div', {'id': 'game_area_purchase', 'class': 'game_area_purchase'})
            game_price = ''

            free_to_play_divs = game_div_price.find_all('div', {'class': 'game_area_purchase_game'})
            for free_to_play_div in free_to_play_divs:
                if free_to_play_div.find('div', {'class': 'game_purchase_price price'}):
                    game_price = free_to_play_div.find('div', {'class': 'game_purchase_price price'}).text.strip()
                    break

            if not game_price:
                pay_to_play_divs = game_div_price.find_all('div', {'class': 'game_area_purchase_game_wrapper'})
                for pay_to_play_div in pay_to_play_divs:
                    if pay_to_play_div.find('div', {'class': 'game_purchase_price price', 'data-price-final': True}):
                        game_price = pay_to_play_div.find('div', {'class': 'game_purchase_price price',
                                                                  'data-price-final': True}).text.strip()
                        break

            pay_with_discount_div = None
            pay_with_discount_divs = game_div_price.find_all('div', {'class': 'game_area_purchase_game_wrapper'})
            for pay_with_discount_div in pay_with_discount_divs:
                if pay_with_discount_div.find('div', {'class': 'discount_final_price'}):
                    discount_final_price = pay_with_discount_div.find('div', {'class': 'discount_final_price'})
                    game_price = discount_final_price.text.strip()
                    break

            rating = soup.find('meta', {'itemprop': 'ratingValue'})['content']
            span_tags = soup.find_all('span', {'class': 'nonresponsive_hidden responsive_reviewdesc'})
            positive_review = span_tags[-1].text.strip().split(' ')[1]
            review_count = soup.find('meta', {'itemprop': 'reviewCount'})['content']
            writer.writerow([game_name, other_game,', '.join(developer_name), ', '.join(publisher_name) , game_genre, ', '.join(platforms),
                             ','.join(style_genre), release_date, game_price, rating, positive_review, review_count])
        except (AttributeError, TypeError):
            continue