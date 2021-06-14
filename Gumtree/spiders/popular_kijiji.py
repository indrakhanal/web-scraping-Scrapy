import scrapy
from scrapy.selector import Selector
from ..items import PopularKijiji


class KijjiSpider(scrapy.Spider):
    name = 'free'
    allowed_domains = ['kijiji.ca']

    start_urls = [
        'https://www.kijiji.ca/b-british-columbia/l9007?price-type=swap-trade',
    ]

    def parse(self, response, **kwargs):
        data_loaded = response.css('div.container-results:nth-child(3)')
        main_url = str('https://www.kijiji.ca')
        # image_url = 'https:'
        item = PopularKijiji()
        for data in data_loaded:
            # item['heading'] = 'Free Stuff'
            text = data.css('a ::text').getall()
            text_list = []
            for texts in (text[2:-11]):
                text_list.append(texts)
            # item['title'] = text_list
            url = data.css('a::attr(href)').getall()
            image = data.css('img::attr(src)').getall()
            url_list = []
            image_list = []

            for images in image:
                image_list.append(images)
            # item['image'] = image_list

            for urls in url:
                sub_urls = main_url+urls
                url_list.append(sub_urls)
            # item['url'] = url_list
            description = data.css('.description ::text').getall()
            description_list = []
            for desc in description:
                description_list.append(desc)
            item['description'] = description_list
            limit = (len(text[2:-11]))
            i = 0
            while i != limit:
                item['heading'] = 'swap/trade'
                item['title'] = text_list[i]
                item['url'] = url_list[i]
                item['image'] = image_list[i]
                item['description'] = description_list[i]
                yield item
                i += 1

