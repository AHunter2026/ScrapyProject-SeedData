import scrapy
import re


class Johnnys(scrapy.Spider):
    name = '2026SpringBuy'
    allowed_domains = ['johnnyseeds.com']
    start_urls = [
        'https://www.johnnyseeds.com/vegetables/onions/bunching-onions/deep-purple-onion-seed-491.html',
        'https://www.johnnyseeds.com/vegetables/tomatoes/heirloom-tomatoes/san-marzano-ii-organic-tomato-seed-3405G.html',
        'https://www.johnnyseeds.com/vegetables/lettuce/butterhead-lettuce-boston/milagro-organic-lettuce-seed-4215G.html',
        'https://www.johnnyseeds.com/vegetables/chicory/endive/curlesi-organic-endive-seed-3448G.html',
        'https://www.johnnyseeds.com/vegetables/chicory/radicchio/perseo-radicchio-seed-3099.html',
        'https://www.johnnyseeds.com/vegetables/chicory/radicchio/bel-fiore-radicchio-seed-3113.html',
        'https://www.johnnyseeds.com/vegetables/cucumbers/seedless-and-thin-skinned-cucumbers/diva-cucumber-seed-2198.html',
        'https://www.johnnyseeds.com/vegetables/cucumbers/specialty-cucumbers/quick-snack-f1-cucumber-seed-5158.html',
        'https://www.johnnyseeds.com/vegetables/radishes/round-radishes/sora-organic-radish-seed-612G.html',
        'https://www.johnnyseeds.com/vegetables/radishes/round-radishes/donato-f1-radish-seed-4910.html',
        'https://www.johnnyseeds.com/vegetables/greens/specialty-greens/red-leaf-vegetable-amaranth-specialty-green-seed-516.html',
        'https://www.johnnyseeds.com/vegetables/lettuce/romaine-lettuce-cos/tendita-lettuce-seed-4595.html',
        'https://www.johnnyseeds.com/vegetables/chinese-cabbage/citrus-f1-chinese-cabbage-seed-4271.html',
        'https://www.johnnyseeds.com/vegetables/chicory/italian-dandelion/italiko-red-italian-dandelion-seed-3358.html',
        'https://www.johnnyseeds.com/vegetables/chicory/italian-dandelion/catalogna-special-italian-dandelion-seed-375.html',
        'https://www.johnnyseeds.com/vegetables/chicory/endive/sempre-bianca-endive-seed-4265.html',
        'https://www.johnnyseeds.com/vegetables/chicory/escarole/eros-organic-escarole-seed-2811G.html'
    ]

    def parse_accordion(self, response):
        """Extract data from accordion sections"""
        accordion_html = response.css('div.c-accordion__body.s-lgc-pdp-content').get()

        if not accordion_html:
            return {}

        # Split by h2 tags to get sections
        sections = re.split(r'<h2>', accordion_html)

        accordion_data = {}
        for section in sections[1:]:  # Skip first empty element
            if '</h2>' in section:
                # Extract key and value
                key, value = section.split('</h2>', 1)
                key = key.strip().replace(':', '').lower().replace(' ', '_')
                # Clean HTML tags from value
                value = re.sub(r'<[^>]+>', '', value).strip()
                accordion_data[key] = value

        return accordion_data

    def parse(self, response):
        # Get product title
        title = response.css('h1.product-name::text').get()
        subtitle = response.css('span.product-alternate-name::text').get()
        full_title = f"{title.strip()} {subtitle.strip()}" if title and subtitle else None

        # Get the main facts list
        facts_dl = response.css('dl.c-facts__list')
        facts_dict = {}

        if facts_dl:
            facts_dl = facts_dl[0]
            dt_elements = facts_dl.css('dt')
            dd_elements = facts_dl.css('dd')

            # Puts the terms and definitions together
            for dt, dd in zip(dt_elements, dd_elements):
                term = dt.css('h3::text').get()
                defn = dd.css('h4::text').get()
                # If the data isn't in the dt or dd elements, it looks in abbr elements
                if not defn or defn.strip() in [',', '']:
                    defn = ', '.join(dd.css('abbr::text').getall())

                if not defn or not defn.strip():
                    defn = ' '.join(dd.css('::text').getall()).strip()

                if term and defn:
                    facts_dict[term.strip()] = defn.strip()

        # Get germination guide image
        germination_image = response.css('img.c-facts__supplementary_image::attr(src)').get()
        if germination_image:
            # Convert relative URL to absolute URL
            germination_image = response.urljoin(germination_image)

        # Get accordion data
        accordion_info = self.parse_accordion(response)

        # Yield the data
        yield {
            'Name': full_title,
            'Scientific_name': accordion_info.get('scientific_name'),
            'Days_to_maturity': facts_dict.get('Days To Maturity'),
            'Life_cycle': facts_dict.get('Life Cycle'),
            'Disease_resistance': facts_dict.get('Disease Resistance Codes'),
            'Hybrid_status': facts_dict.get('Hybrid Status'),
            'image_urls': [germination_image] if germination_image else [],
            'Notes': accordion_info.get('culture')
        }