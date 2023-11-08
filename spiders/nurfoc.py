import scrapy
import scrapy.http
import re
from scraper.items import NurfocItem
from scrapy.http import FormRequest

#table_1 > tbody:nth-child(2)
#table_1 > tbody:nth-child(2)
# /html/body/div[1]/div/main/div/div/div[1]/div/table/tbody
class NurfocSpider(scrapy.Spider):
    """ based off the following shell commands:
    scrapy shell https://nuforc.org/ndx/?id=loc
    response.css("a::attr(href)").getall()
    view(response)
    """
    name = "nurfoc"
    start_urls = ["https://nuforc.org/ndx/?id=loc"]
    custom_settings = {
        'MONGOPIPELINE_ENABLED': True
    }
    headers = {
            "authority": "nuforc.org",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://nuforc.org",
            "pragma": "no-cache",
            "referer": "https://nuforc.org/subndx/?id=lNS",
            "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
    body = 'draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=Link&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=Occurred&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=City&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=State&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=Country&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=Shape&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=Summary&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=Reported&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=Posted&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=HasImage&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=100000&search%5Bvalue%5D=&search%5Bregex%5D=false&wdtNonce=1f9da5a0c8'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        table = response.css("a::attr(href)").getall()
        
        # parse for "subndx?id="
        links = [f"https://nuforc.org/{l}" for l in table if "/subndx" in l]

        for link in links:
            page_id = link.split("=")[-1]
            geo_area = "State" if page_id.startswith("l") else "Country"
            #remove the l or c from the page_id
            page_id = page_id[1:]
            url = f'https://nuforc.org/wp-admin/admin-ajax.php?action=get_wdtable&table_id=1&wdt_var1={geo_area}&wdt_var2={page_id}'
            yield scrapy.Request(
                url=url,
                method='POST',
                dont_filter=True,
                headers=self.headers,
                body=self.body,
                callback=self.parse_summary
            )
    # def second_urls(self, response: scrapy.http.Response):
    def parse_summary(self, response):
        # This will print the entire content of the response to the console/log.
        # It's a simple way to check what the response data looks like.
        #load response text into a json object
        data = response.json()
        #save the data to a file
        data_rows = data['data']
        for index, row in enumerate(data_rows):
            # each index corresponds to a row in the table,
            item = NurfocItem()
            item["link"] = row[0]
            item["occured"] = row[1]
            item["city"] = row[2]
            item["state"] = row[3]
            item["country"] = row[4]
            item["shape"] = row[5]
            item["summary"] = row[6]
            item["reported"] = row[7] 
            item["posted"] = row[8]
            item["image"] = row[9]

            match = re.search(r'\?id=(\d+)', item["link"])
            if match:
                item['sighting_id'] = match.group(1)
            else:
                item['sighting_id'] = None
                yield item
            url = f"https://nuforc.org/sighting/?id={item['sighting_id']}"
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse_detailed,
                cb_kwargs={'item': item}
            )
    def parse_detailed(self, response, item: NurfocItem=None):
        # Convert the response to text
        html_content = response.text
        
        # Use regular expression to extract the desired text after "Posted:" and before the copyright notice
        # This pattern looks for "Posted:" followed by a date, and captures text until it reaches the copyright notice
        pattern = r'Posted:</b>\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}<br><br><br>(.*?)<p style="color: white;'
        match = re.search(pattern, html_content, re.DOTALL)
        
        # If a match is found, clean up the matched text
        if match:
            # The captured text may contain HTML tags (`<br>`, `<p>`, etc.) which we remove
            notes = re.sub(r'<.*?>', '', match.group(1)).strip()
        else:
            # If nothing is found, set notes to None or an empty string
            notes = None

        # Assign the notes to the item
        item['notes'] = notes
        
        # Yield the item
        yield item


    def parse_table(self, response: scrapy.http.Response):
        """Extracting data from the table on the 'subndx?id=' pages
            this table contains the links to the actual reports, along with
            cursory information about the report.

        Args:
            response (scrapy.http.Response): _description_

        Yields:
            _type_: _description_
        """
        table_rows = response.xpath("//tbody//tr")
        for row in table_rows:
            item = NurfocItem()
            item["link"] = row.css("a::attr(href)").get()
            item["occured"] = row.css("td:nth-child(2)").get()
            item["city"] = row.css("td:nth-child(3)::text").get()
            item["state"] = row.css("td:nth-child(4)::text").get()
            item["country"] = row.css("td:nth-child(5)::text").get()
            item["shape"] = row.css("td:nth-child(6)::text").get()
            item["summary"] = row.css("td:nth-child(7)::text").get()
            item["reported"] = row.css("td:nth-child(8)::text").get()
            item["posted"] = row.css("td:nth-child(9)::text").get()
            item["image"] = row.css("td:nth-child(10)::text").get()
            yield item
        
        