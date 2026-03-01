# News Scan Bot

A web scraping application that crawls news websites and extracts article information using Scrapy and Flask.

## Features

- Multi-threaded proxy validation
- News article crawling from multiple Indian news sources
- Flask REST API for initiating crawls
- Proxy rotation for anonymized requests
- Structured data extraction using Scrapy ItemLoader

## Project Structure

```
News-Scan-Bot/
├── app.py                          # Flask application entry point
├── checkProxies.py                 # Proxy validation utility
├── main.py                         # Proxy testing script
├── validProxies.txt                # List of valid proxies (auto-generated)
├── README.md                       # This file
├── LICENSE                         # GPL v3 License
└── news_website_crawler/
    ├── scrapy.cfg                  # Scrapy configuration
    └── news_website_crawler/
        ├── settings.py             # Scrapy settings
        ├── items.py                # Item definitions
        ├── pipelines.py            # Data processing pipelines
        ├── middlewares.py          # Custom middleware
        ├── output.json             # Crawled data output
        └── spiders/
            └── news_crawling_spider.py  # Main spider implementation
```

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd News-Scan-Bot
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install scrapy flask requests
   ```

4. **Create a proxy list file** (optional)
   ```bash
   # Create validProxies.txt with proxy addresses, one per line
   # Example format:
   # 192.168.1.1:8080
   # 10.0.0.1:3128
   echo "# Add your proxies here" > validProxies.txt
   ```

## Usage

### 1. Validate Proxies

Check which proxies in your list are working:

```bash
python checkProxies.py
```

This script:
- Reads proxies from `proxyList.txt`
- Tests each proxy against `http://ipinfo.io/json`
- Prints working proxies to console
- Saves valid proxies to `validProxies.txt`

### 2. Test Proxies with Sample Sites

```bash
python main.py
```

This script tests the proxies against sample book store websites.

### 3. Run the Flask API Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Initiate a Crawl via API

Send a POST request to the API:

```bash
curl -X POST http://localhost:5000/verify_news \
  -H "Content-Type: application/json" \
  -d '{"news_query": "politics"}'
```

Response:
```json
{
  "message": "Crawling initiated."
}
```

### 5. Run Scrapy Directly

To crawl news articles directly using Scrapy:

```bash
cd news_website_crawler
scrapy crawl mycrawler
```

## Configuration

### Supported News Websites

The spider crawls from these Indian news sources:
- aajtak.in
- abpnews.com
- timesofindia.indiatimes.com
- news18.com
- india.com

### Customizing Selectors

To extract different data, edit the CSS selectors in `news_website_crawler/news_website_crawler/spiders/news_crawling_spider.py`:

```python
loader.add_css('title', 'h1::text')           # Update to match actual HTML
loader.add_css('content', 'p::text')          # Update to match actual HTML
loader.add_css('date', '.article-date::text') # Update to match actual HTML
```

### Adjusting Scrapy Settings

Edit `news_website_crawler/news_website_crawler/settings.py`:

```python
DOWNLOAD_DELAY = 3              # Delay between requests (seconds)
CONCURRENT_REQUESTS = 16        # Parallel requests
USER_AGENT = '...'             # Custom user agent
ROBOTSTXT_OBEY = True          # Respect robots.txt
```

## Troubleshooting

### Issue: "validProxies.txt not found"
**Solution:** The application gracefully handles missing proxy files. Create an empty file or populate `proxyList.txt` and run `checkProxies.py`.

### Issue: "No module named 'news_website_crawler'"
**Solution:** Make sure you're running from the correct directory. The project structure requires importing from the root directory.

### Issue: Proxies not working
**Solution:** Verify proxies with `checkProxies.py` first. Free proxies may be unstable. Consider using paid proxy services.

### Issue: No data being extracted
**Solution:** The CSS selectors in `parse_article()` need to match your target website's HTML structure. Inspect the webpage and update selectors accordingly.

## Data Output

Crawled data is saved in `news_website_crawler/news_website_crawler/output.json` with the following structure:

```json
{
  "title": "Article Title",
  "content": "Article content text...",
  "source": "https://news-website.com/article-url",
  "date": "2024-01-15"
}
```

## API Endpoints

### POST /verify_news
Initiates a web crawl for news articles.

**Request:**
```json
{
  "news_query": "politics"
}
```

**Response:**
```json
{
  "message": "Crawling initiated."
}
```

**Error Response:**
```json
{
  "error": "description of error"
}
```

## Architecture

### Components

1. **Scrapy Spider** (`news_crawling_spider.py`)
   - Handles web crawling
   - Manages proxy rotation
   - Extracts structured data

2. **Flask App** (`app.py`)
   - REST API endpoint
   - Request validation
   - Error handling

3. **Middlewares** (`middlewares.py`)
   - Proxy rotation middleware
   - Spider and downloader middleware

4. **Data Items** (`items.py`)
   - NewsItem: Structured data model for articles

## Dependencies

- **Scrapy** - Web scraping framework
- **Flask** - Web framework for API
- **Requests** - HTTP library
- **Twisted** - Async networking library (Scrapy dependency)

## Performance Tips

1. **Adjust DOWNLOAD_DELAY** in settings.py to control crawling speed
2. **Use multiple proxies** to distribute requests
3. **Tune CONCURRENT_REQUESTS** based on your system resources
4. **Implement request deduplication** to avoid redundant crawls

## Legal & Ethical Considerations

- Always check the website's `robots.txt` before crawling
- Respect website's Terms of Service
- Don't overload servers with too many requests
- This project is licensed under GPL v3 - see LICENSE file

## Future Enhancements

- [ ] Database storage for crawled data
- [ ] Advanced data filtering and processing pipeline
- [ ] Scheduled crawling with task queue (Celery)
- [ ] Machine learning for content classification
- [ ] Web dashboard for monitoring crawls
- [ ] Advanced proxy management with health checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For issues and questions:
- Check the Troubleshooting section
- Review Scrapy documentation: https://docs.scrapy.org/
- Flask documentation: https://flask.palletsprojects.com/
