from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)

@app.route('/verify_news', methods=['POST'])
def verify_news():
    try:
        news_query = request.json.get('news_query')
        if not news_query:
            return jsonify({"error": "news_query is required"}), 400
        
        process = CrawlerProcess(get_project_settings())
        process.crawl("mycrawler", news_query=news_query)
        process.start()
        return jsonify({"message": "Crawling initiated."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
