import scrapy, requests
import random
from ..items import ItCompanyDetail
import time
import re
import sys
from requests_html import HTMLSession


class NewsLand(scrapy.Spider):
    name = 'newsland'
    allowed_domains = ['www.goodfirms.co']

    def start_requests(self):
        urls = ['https://www.goodfirms.co/it-services/new-zealand']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        all_item = response.css('.directory-content')
        for data in all_item:
            company_name = data.css('div.listing-name-tag h3 a::text').getall()
            location_name = data.css('div.firm-location span::text').getall()
            link = data.css('div.firms-r a::attr(href)').getall()
            print(len(company_name), len(location_name), len(link))
            EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
            session = HTMLSession()
            i=0
            while i!= len(link)-1:
                r = session.get(link[i])
                r.html.render()
                email_list = []
                for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
                    company_email = re_match.group()
                    email_list.append(company_email)

                clean_email_set = set(email_list)
                clean_list = list(clean_email_set)
                if len(clean_list) == 0:
                    r = session.get(link[i]+str('/contact'))
                    r.html.render()
                    email_list = []

                    for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
                        company_email = re_match.group()
                        email_list.append(company_email)

                    clean_email_set = set(email_list)
                    clean_list = list(clean_email_set)

                individual_company_name = company_name[i]
                item = ItCompanyDetail()
                item['company_Name'] = individual_company_name
                item['company_Email'] = clean_list
                item['company_Location'] = location_name[i]
                item['company_website_link'] = link[i]
                yield item
                i+=1