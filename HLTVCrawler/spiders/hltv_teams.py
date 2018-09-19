import scrapy

class MySpider(scrapy.Spider):
    name = 'hltv_teams'
    start_urls = [
        'https://www.hltv.org/results'
    ]

    def parse(self, response):
        matchPageLinks = response.css('.results-holder .result-con a::attr(href)').extract()
        for link in matchPageLinks:
            nextUrl = response.urljoin(link)
            yield scrapy.Request(nextUrl, callback=self.parseMatchPage)
        
        nextPage = response.css('.pagination-next::attr(href)').extract_first()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)

    
    def parseMatchPage(self, response):
        teamPages = response.css('.teamsBox .team a::attr(href)').extract()
        for link in teamPages:
            nextUrl = response.urljoin(link)
            yield scrapy.Request(nextUrl, callback=self.parseTeamPage)
    
    def parseTeamPage(self, response):
        yield {
            'name': response.css('.profile-team-name::text').extract_first(),
            'players': response.css('.teamProfile .playerFlagName .bold::text').extract()
        }