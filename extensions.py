import requests
import lxml.html
import json


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def get_currencys():
        return {
            'RUB': ['рубль', 'рубли', 'рублей'],
            'USD': ['доллар', 'доллары', 'долларов'],
            'EUR': ['евро', 'евров']
        }

    @staticmethod
    def get_price(base, quote, amount):
        currencys = Parser.get_currencys()

        for currency in currencys:
            if base in currencys[currency]:
                base = currency
            elif quote in currencys[currency]:
                quote = currency

        try:
            amount = float(amount)
        except:
            raise APIException("Введено некорректное число.")

        if not base in Parser.get_currencys() or not quote in Parser.get_currencys():
            raise APIException("Введена неизвестная валюта или они равны.")
        if base == quote:
            raise APIException("Введенные валюты равны.")
        url = f"https://www.calc.ru/kurs-{quote}-{base}.html?text_quantity={amount}"
        html = requests.get(url).content
        tree = lxml.html.document_fromstring(html)
        title = tree.xpath("//div[@class='t18']/strong//text()")[0].split('=')[1].replace(base, '').strip()

        text = f"Цена {amount} {quote} в {base} равна {title}. "
        response = json.dumps({'message': text})
        return response


class APIException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message