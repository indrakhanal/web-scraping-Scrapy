import scrapy
from scrapy.item import Item, Field


class GumtreeItem(Item):
    category = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()


class KijijiItem(Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    url = scrapy.Field()
    sub_url = scrapy.Field()


class ItemWithLocation(Item):
    location = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    # people_choice = scrapy.Field()
    # popular = scrapy.Field()
    # popular_buy_shell = scrapy.Field()


class PopularKijiji(Item):
    heading = scrapy.Field()
    title = scrapy.Field()
    subtitle = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()


class BuySell(Item):
    location = scrapy.Field()
    product_name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()


class CarVehicles(Item):
    location = scrapy.Field()
    Name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    related_images = scrapy.Field()
    url = scrapy.Field()
    detail = scrapy.Field()
    Includes = scrapy.Field()


class ItCompanyDetail(Item):
    company_Name = scrapy.Field()
    company_Location = scrapy.Field()
    company_Email = scrapy.Field()
    company_website_link = scrapy.Field()


