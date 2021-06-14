import scrapy, requests
import random
from ..items import CarVehicles
import time


class CarDetail(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['kijiji.ca']

    # def start_requests(self):
    #     i=48
    #     while i!=52:
    #         urls = [f'https://www.kijiji.ca/b-cars-vehicles/british-columbia/page-{i}/c27l9007']
    #         for url in urls:
    #             yield scrapy.Request(url=url, callback=self.parse)
    #             time.sleep(60)
    #             i+=1

    start_urls = ['https://www.kijiji.ca/b-cars-vehicles/british-columbia/page-100/c27l9007']

    def parse(self, response, **kwargs):
        all_item = response.css('div.container-results:nth-child(3)')
        for data in all_item:
            # new_div = data.css('div.info')
            link = data.css('div.info div.title a::attr(href)').getall()
            url = ["https://www.kijiji.ca"+str(i) for i in link]
            limit = len(url[:-3])-1
            for i in range(limit):
                request = scrapy.Request(url[i], callback=self.parse_car, meta={'url': url[i]})
                yield request

    def parse_car(self, response, **kwargs):
        car_detail = response.css('#AttributeList')
        title = response.css('div.mainColumn-1522885425 h1::text').get()
        location = response.css('div.locationContainer-2867112055 span[class="address-3617944557"] ::text').get()
        url = response.meta['url']
        detail = car_detail.css('ul[class="itemAttributeList-1090551278"] li dl dt ::text').getall()
        relavent = car_detail.css('ul[class="itemAttributeList-1090551278"] li dl dd ::text').getall()
        includes = car_detail.css('ul[class="itemAttributeList-1090551278"] li span::text').getall()
        description = response.css('div.descriptionContainer-3261352004 ::text').getall()
        price = response.css('div.mainColumn-1522885425 span[itemprop="price"] ::text').get()
        related_images = response.css('div.heroImageContainer-3252084013 img::attr(src)').getall()

        try:
            detail = [s.replace(".", "_") for s in detail]
            detail = [r.replace(" ", "_") for r in detail]
        except:
            detail = detail
        try:
            relavent = [s.replace(".", "") for s in relavent]
        except:
            relavent = relavent

        relavent_length = len(relavent)
        detail_length = len(detail)
        if relavent_length == detail_length:
            new_detail_dict=dict(zip(detail, relavent))
        elif relavent_length>detail_length:
            del relavent[0]
            new_detail_dict=dict(zip(detail, relavent))
        else:
            del detail[0]
            new_detail_dict = dict(zip(detail, relavent))
        detail_in_list = []
        detail_in_list.append(new_detail_dict)

        item = CarVehicles()
        item['Name'] = title
        item['location'] = location
        item['price'] = price
        item['related_images'] = related_images
        item['url'] = url
        item['description'] = description
        item['detail'] = detail_in_list
        item['Includes'] = includes
        print(type(item['Name']))
        if item['Name'] != 'None':
            yield item
        else:
            print('null item seen so break')

