from requests_html import HTMLSession
import pandas as pd
import time

print('initialize session')

s = HTMLSession()
items = []

print('finished!')

def request(url):
    r = s.get(url)
    r.html.render(sleep=1)
    return r.html.xpath('//*[@id="listing-container"]', first=True)


def parse(products, categoryName):
    for item in products.absolute_links:
        if "#Opinie" in item:
            continue
        print(item)
        r = s.get(item)
        try:
            name = r.html.find('h1.sc-1bker4h-4', first=True).text
        except:
            name = 'none'
        try:
            price = r.html.find('div.sc-n4n86h-4', first=True).text
        except:
            price = '4 899,00 zł'
        try:
            img = r.html.find('img.sc-1tblmgq-1', first=True).attrs.src
        except:
            img = 'none'
        try:
            rating = r.html.find('span.sc-1cbpuwv-1', first=True).text
        except:
            rating = '1,0'
        print(name, price, img, rating)
        # try:
        #     r.html.find('span.sc-fvs7b3-1')
        #     stock = 'in stock'
        # except:
        #     stock = 'out of stock'

        item = {
            'name': name,
            # 'subtext': subtext,
            'price': price,
            'rating': rating,
            # 'stock': stock
            'category': categoryName
        }
        items.append(item)
        time.sleep(0.1)



def output(categoryName):
    df = pd.DataFrame(items)
    df.to_csv(categoryName + '.csv', index=False)
    print('Saved to CSV file.')


def extract_data_from_category(url, categoryName):
    global items
    items = []
    x = 1
    print('scrapping of ' + categoryName + ' started! ')
    while x == 1:
        try:
            products = request(url + f'?page={x}')
            print(f'Getting items from page {x} in category' + categoryName)
            parse(products, categoryName)
            print('Total Items: ', len(items))
            x = x + 1
            time.sleep(2)
            if len(items) > 400:
                break
        except:
            print('No more items!')
            break
    output(categoryName)


print('beginning of scrapping process')
extract_data_from_category('https://www.x-kom.pl/g-2/c/159-laptopy-notebooki-ultrabooki.html',
                           'laptopy-notebooki-ultrabooki')
extract_data_from_category('https://www.x-kom.pl/g-4/c/1590-smartfony-i-telefony.html', 'smartfony-i-telefony')