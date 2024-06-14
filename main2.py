import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['tradebox.shop']
    start_urls = ['https://tradebox.shop']

    def parse(self, response):
        # link = response.css('div.card.card_4 a::attr(href)').getall()
        # print(link)
        for link in response.css("div.card.card_4 a::attr(href)").getall():
            yield response.follow(link, callback=self.parse_page)


    def parse_page(self, response):
        category = response.css('div.breadcrumbs ul li a::text').getall()
        
        yield {
            "title": response.css('div.product__content h1::text').get(),
            "category" : category[len(category) -1],
            "price": response.css("div.product__price span::text").get(),
            "info": response.css("*[itemprop='description'] span::text").getall()[2::],
            "link": response.request.url
        }