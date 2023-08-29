from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import random

class NewsCrawlingSpider (CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["aajtak.in", "abpnews.com", "timesofindia.indiatimes.com", "indiatimes.com",
                       "news18.com", "india.com"]
    websites = ["http://www.aajtak.in/", "http://www.abplive.com/", "http://timesofindia.indiatimes.com/",
                  "http://www.indiatimes.com/", "http://www.news18.com/", "http://www.india.com/"]

    # PROXY_SERVER = "127.0.0.1"

    rules = (
        # Rule(LinkExtractor(allow="catalogue/category")),
        # Rule (LinkExtractor (allow="catalogue", deny="category"), callback="parse_item")
        Rule(LinkExtractor(allow=f'/article/'), callback='parse_article'),
        
        # Pagination
        Rule(LinkExtractor(allow=f'/page/\d+/')),

        # Categories
        Rule(LinkExtractor(allow=f'/politics/'), callback='parse_article'),
        Rule(LinkExtractor(allow=f'/sports/'), callback='parse_article'),

    )

    def get_random_proxy(self):
        # return random.choice(settings.PROXY_LIST)
        return random.choice(self.settings.get('PROXY_LIST', []))

    def start_requests(self):
        for website in self.websites:
            yield scrapy.Request(url=website, callback=self.parse, meta={'proxy': self.get_random_proxy()})

    # Add a method to search related news based on the input query
    # def search_related_news(self, news_query):
    #     # Implement logic to search for related news on the crawled websites
    #     # You can use Scrapy's item loaders to structure the results
    #     results = []
    #     for url in self.websites:
    #         yield scrapy.Request(url=url, callback=self.parse_related_news, meta={'news_query': news_query})
            
    # def parse_related_news(self, response):
    #     news_query = response.meta['news_query']
    #     # Implement logic to search for related news based on the news_query
    #     # You can use response.css or response.xpath to select relevant elements
    #     # Create an ItemLoader to structure the extracted data
    #     loader = ItemLoader(item=NewsItem(), response=response)
        
    #     # Extract relevant information using CSS selectors
    #     loader.add_css('title', 'your-css-selector-for-title')
    #     loader.add_css('content', 'your-css-selector-for-content')
    #     loader.add_css('source', 'your-css-selector-for-source')
    #     loader.add_css('date', 'your-css-selector-for-date')
        
    #     results.append(loader.load_item())
    #     # Continue parsing other news articles if needed        
    #     return results
    
    def parse_article(self, response):
        # Implement your logic to parse individual news articles
        # For example, use response.css or response.xpath to extract data
        # Create an ItemLoader to structure the extracted data
        if response.status == 200:
            loader = ItemLoader(item=NewsItem(), response=response)
        elif response.status == 403:
            self.logger.warning("Received a 403 Forbidden response for URL: %s", response.url)
        else:
            self.logger.warning("Received an unexpected response for URL %s with status code %d", response.url, response.status)

        # Extract relevant information using CSS selectors
        loader.add_css('title', 'your-css-selector-for-title')
        loader.add_css('content', 'your-css-selector-for-content')
        loader.add_css('source', 'your-css-selector-for-source')
        loader.add_css('date', 'your-css-selector-for-date')

        yield loader.load_item()

    # def parse_item (self, response):
    #     yield {
    #         "title": response.css(".product_main h1::text").get(),
    #         "price": response.css(".price_color::text").get(),
    #         "availability": response.css(".availability::text")[1].get().replace("\n", "").replace(" ", ""),
    #     }