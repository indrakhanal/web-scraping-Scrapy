import scrapy
from scrapy.selector import Selector
from ..items import GumtreeItem


class GumtreeSpider(scrapy.Spider):
    name = 'gumtree'
    allowed_domains = ['gumtree.com.au']

    start_urls = [
        'https://www.gumtree.com.au/s-automotive/c21159',
        ]

    def parse(self, response, **kwargs):
        data_loaded = response.css('.search-results-page__user-ad-collection')
        main_url = str('https://www.gumtree.com.au')
        for data in data_loaded:
            item = GumtreeItem()
            item['category'] = 'Automotive'
            title = data.css('p span[class="user-ad-row-new-design__title-span"] ::text').getall()
            image = data.css('img[class="user-ad-image__thumbnail image image--is-visible"] ::attr(src)').getall()
            url = data.css('a[class="user-ad-row-new-design user-ad-row-new-design--highlight user-ad-row-new-design--featured-or-premium link link--base-color-inherit link--hover-color-none link--no-underline"] ::attr(href)').getall()
            location = data.css('.user-ad-row-new-design__location ::text').getall()
            description = data.css('p[class="user-ad-row-new-design__description-text"] ::text').getall()

            title_list = []
            for titles in title:
                clean_title = titles.strip()
                title_list.append(clean_title)

            image_list = []
            for images in image:
                image_list.append(images)

            url_list = []
            for urls in url:
                full_url = main_url+urls
                url_list.append(full_url)

            location_list = []
            for locations in location:
                clean_location = locations.strip()
                location_list.append(clean_location)

            description_list = []
            for descriptions in description:
                clean_description = descriptions.strip()
                description_list.append(clean_description)
            print(len(title_list))
            print(len(url_list))
            print(len(image_list))
            print(len(title_list))
            print()
            yield item
