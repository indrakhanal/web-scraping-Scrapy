import scrapy
from ..items import BuySell


class KijjiSpider(scrapy.Spider):
    name = 'buySell'
    allowed_domains = ['kijiji.ca']

    def start_requests(self):
        index = 95
        while index != 110:
            urls = [
                f'https://www.kijiji.ca/b-buy-sell/british-columbia/page-{index}/c10l9007',
            ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
            index += 1

    #     start_urls = [
    #         f'https://www.kijiji.ca/b-buy-sell/british-columbia/page-{index}/c10l9007',
    #     ]

    def parse(self, response, **kwargs):
        data_loaded = response.css('div.container-results:nth-child(3)')
        main_url = str('https://www.kijiji.ca')
        # image_url = 'https:'
        item = BuySell()
        for data in data_loaded:
            text = data.css('.title a::text').getall()
            text_list = []
            for texts in text:
                clean_text = texts.strip()
                text_list.append(clean_text)
            url = data.css('.title a::attr(href)').getall()
            image = data.css('.image img::attr(data-src)').getall()
            url_list = []
            image_list = []

            for images in image:
                image_list.append(images)

            for urls in url:
                sub_urls = main_url+urls
                url_list.append(sub_urls)
            location_list = []
            location = data.css('.location span[class=""]::text').getall()
            for locations in location:
                clean_location=locations.strip()
                location_list.append(clean_location)

            description = data.css('.clearfix .description ::text').getall()
            description_list = []
            for desc in description:
                clean_description = desc.strip()
                description_list.append(clean_description)
            while "" in description_list:
                description_list.remove("")

            price = data.css('.clearfix .price ::text').getall()
            price_list = []

            for prices in price:
                clean_price = prices.strip()
                price_list.append(clean_price)
            print(price_list)
            while "" in price_list:
                price_list.remove("")
            print(len(price_list))
            limit = (len(text))
            i = 0
            while i != limit:
                item['location'] = location_list[i]
                item['product_name'] = text_list[i]
                item['price'] = price_list[i]
                item['url'] = url_list[i]
                item['image'] = image_list[i]
                item['description'] = description_list[i]
                yield item
                i += 1

