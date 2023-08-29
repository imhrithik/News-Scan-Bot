from flask import Flask, request, jsonify
from news_website_crawler.spiders.news_crawling_spider import NewsCrawlingSpider
from news_crawling_spider import NewsCrawlingSpider

app = Flask(__name__)
spider = NewsCrawlingSpider()

@app.route('/verify_news', methods=['POST'])
def verify_news():
    news_query = request.json.get('news_query')
    process = CrawlerProcess(get_project_settings())
    process.crawl("mycrawler", news_query=news_query)
    process.start()
    return jsonify({"message": "Crawling initiated."})
    # results = spider.search_related_news(news_query)
    # return jsonify(results)

if __name__ == '__main__':
    app.run()
