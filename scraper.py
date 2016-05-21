import scrapy
from scrapy.crawler import CrawlerProcess
import scraperwiki
from datetime import datetime

class ConsultationSpider(scrapy.Spider):
    name = "consultation"
    def start_requests(self):
        for lang in ['en', 'tc', 'sc']:
            yield scrapy.Request('http://www.gov.hk/%s/residents/government/publication/consultation/current.htm' % (lang), meta={'lang':lang})


    def parse(self, response):
        table = response.xpath("//div[@class='content']/table")[0]
        rows = table.xpath("tr")
        for row in rows[1:]:
            title_cell, date_cell = row.xpath("td")
            title = title_cell.xpath("a/text()").extract()[0]
            link = title_cell.xpath("a/@href").extract()[0]
            date_str = date_cell.xpath("text()").extract()[0]
            date = datetime.strptime(date_str,"%d.%m.%Y")
            d = {"title": title, "lang":response.meta['lang'], "date": date, "link": link}
            print d
            scraperwiki.sqlite.save(unique_keys=["title", "lang"], data=d)
process = CrawlerProcess()
process.crawl(ConsultationSpider)
process.start()

 
