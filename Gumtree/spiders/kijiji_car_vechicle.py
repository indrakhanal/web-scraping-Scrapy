import scrapy
from ..items import CarVehicles


class KijjiSpider(scrapy.Spider):
    name = 'car'
    allowed_domains = ['kijiji.ca']

    def start_requests(self):
        index = 1
        while index != 100:
            urls = [
                f'https://www.kijiji.ca/b-cars-vehicles/british-columbia/page-{index}/c27l9007',
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
        item = CarVehicles()
        for data in data_loaded:
            text = data.css('.title a::text').getall()
            url = data.css('.title a::attr(href)').getall()
            price = data.css('.info .price ::text').getall()
            image = data.css('.image img::attr(data-src)').getall()
            detail = data.css('.description .details ::text').getall()
            location = data.css('.location span[class=""]::text').getall()
            # description = data.css('.clearfix div[class="description"] ::text').getall()
            dealer_logo = data.css('.dealer-logo img::attr(src)').getall()

            text_list = []
            for texts in text:
                clean_text = texts.strip()
                text_list.append(clean_text)

            image_list = []
            for images in image:
                image_list.append(images)

            url_list = []
            for urls in url:
                sub_urls = main_url+urls
                url_list.append(sub_urls)

            location_list = []
            for locations in location:
                clean_location=locations.strip()
                location_list.append(clean_location)

            # description_list = []
            # for desc in description:
            #     clean_description = desc.strip()
            #     description_list.append(clean_description)
            # while "" in description_list:
            #     description_list.remove("")

            price_list = []
            for prices in price:
                clean_price = prices.strip()
                price_list.append(clean_price)
            while "" in price_list:
                price_list.remove("")

            detail_list = []
            for details in detail:
                clean_detail = details.strip()
                detail_list.append(clean_detail)
            final_detail = [dl.strip() for dl in detail_list]

            dealer_logo_list = []
            for dealer in dealer_logo:
                dealer_logo_list.append(dealer)

            limit = (len(text))
            print(limit, 'limit')
            i = 0
            while i != limit:
                item['location'] = location_list[i]
                item['vehicles_name'] = text_list[i]
                item['price'] = price_list[i]
                item['url'] = url_list[i]
                item['image'] = image_list[i]
                # item['description'] = description_list[i]
                item['dealer_logo'] = dealer_logo_list[i]
                item['detail'] = final_detail[i]
                yield item
                i += 1

            # print(len(description_list), 'description')
            print(len(detail_list), 'detail')
            print(len(text_list), 'name')
            print(len(price_list), 'price')
            print(len(url_list), 'url')
            print(len(image_list), 'image')

