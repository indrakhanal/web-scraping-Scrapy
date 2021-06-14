import scrapy
from scrapy.selector import Selector
from ..items import ItemWithLocation


class KijjiSpider(scrapy.Spider):
    name='kijji'
    allowed_domains = ['kijiji.ca']

    start_urls = [
        'https://www.kijiji.ca/h-alberta/9003',
    ]

    def parse(self, response, **kwargs):
        data_loaded = response.css('div.moduleWrapper-4129463801:nth-child(11)')
        print(data_loaded)
        main_url = str('https://www.kijiji.ca/')
        image_url = 'https:'
        item = ItemWithLocation()

        for data in data_loaded:
            title = data.css('h2 ::text').getall()[1]
            item['title'] = f'{title}'
            url = data.css('a::attr(href)').getall()
            image = data.css('img::attr(src)').getall()
            # item['subtitle'] = data.css('li ul li a::text').getall()
            # sub_url = data.css('li ul li a::attr(href)').getall()
            url_list = []
            image_list = []

            for images in image:
                image_url = image_url+images
                image_list.append(image_url)
            item['image'] = image_list

            for urls in url:
                sub_urls = urls
                url_list.append(sub_urls)
            item['url'] = url_list

            yield item

