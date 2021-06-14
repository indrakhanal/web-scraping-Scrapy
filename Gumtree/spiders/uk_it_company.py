import scrapy, requests
import random
from ..items import ItCompanyDetail
import time
import re
import sys
from requests_html import HTMLSession


class NewsLand(scrapy.Spider):
    name = 'uk'
    allowed_domains = ['www.themanifest.com']

    def start_requests(self):
        urls = ['https://themanifest.com/au/it-services/companies?page=1']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        all_item = response.css('div.view-content:nth-child(2)')
        for data in all_item:
            company_name = data.css('div.provider-profile-info header h3 ::text').getall()
            # location_name = data.css('div.provider-basics-item-label span::text').getall()
            link = data.css('div.profile-visit a::attr(href)').getall()
            print(len(company_name), len(link))
            company_list = []
            for comp in company_name:
                clean_comp = comp.strip()
                company_list.append((clean_comp))

            while "" in company_list:
                company_list.remove("")

            clean_company_list = company_list
            EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
            session = HTMLSession()
            i=8
            while i!= len(link)-1:
                r = session.get(link[i])
                r.html.render()
                email_list = []
                for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
                    company_email = re_match.group()
                    email_list.append(company_email)

                clean_email_set = set(email_list)
                clean_list = list(clean_email_set)
                # if len(clean_list) == 0:
                #     r = session.get(link[i]+str('/contact'))
                #     r.html.render()
                #     email_list = []
                #
                #     for re_match in re.finditer(EMAIL_REGEX, r.html.raw_html.decode()):
                #         company_email = re_match.group()
                #         email_list.append(company_email)
                #
                #     clean_email_set = set(email_list)
                #     clean_list = list(clean_email_set)

                # individual_company_name = company_name[i]
                item = ItCompanyDetail()
                item['company_Name'] = clean_company_list[i]
                item['company_Email'] = clean_list
                # item['company_Location'] = location_name[i]
                item['company_website_link'] = link[i]
                yield item
                i+=1