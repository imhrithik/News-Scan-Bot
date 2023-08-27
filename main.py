import requests

with open("validProxies.txt", "r") as f:
    proxies = f.read().split("\n")

sites_to_check = ["http://books.toscrape.com/",
                    "http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html",
                    "http://books.toscrape.com/catalogue/category/books/history_32/index.html"]

counter = 0

for site in sites_to_check:
    try:
        print(f"Using the proxy: {proxies[counter]}")
        res = requests.get(site, proxies={  "http": proxies[counter],
                                            "https": proxies[counter] })
        print(res.status_code)
        # print(res.text)

    except:
        print("Failed")
    finally:
        counter = (counter + 1) % len(proxies)
        # counter += 1
        # counter % len(proxies)