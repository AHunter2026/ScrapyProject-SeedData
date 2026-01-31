# Project Overview

This project uses Scrapy to scrape seed product information (scientific names, known names, descriptors, growing specifications and disease resistance) from various seed company websites. The scraped data is exported to CSV format for easy analysis and reference.

## Features

- Scrapes detailed seed product information including:
  - Product title and Latin/botanical names
  - Days to maturity
  - Life cycle (annual, biennial, perennial)
  - Disease resistance codes
  - Hybrid status
  - Product features and specifications
- Automatic CSV export with configurable field ordering
- URL tracking for reference back to source pages

## Project Structure

```
ScrapyProject-SeedData/
├── scrapy.cfg                 # Scrapy configuration file
└── SeedInfo/                  # Main project directory
    ├── __init__.py
    ├── items.py              # Data structure definitions
    ├── middlewares.py        # Custom middlewares
    ├── pipelines.py          # Data processing pipelines
    ├── settings.py           # Project settings
    └── spiders/              # Spider directory
        ├── __init__.py
        └── johnnys.py # First website scrape
```

## Prerequisites

- Python 3.14.2 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd C:/Users/USERNAME/PycharmProjects/ScrapyProject-SeedData
   ```

2. **Install Scrapy:**
   ```bash
   py -m pip install scrapy
   ```

## Configuration

### CSV Export Settings

Configure CSV export in `settings.py`:

```python
FEEDS = {
    'output_filename.csv': {
        'format': 'csv',
        'overwrite': True,  # Automatically overwrite existing files
    }
}

# Control column order in CSV output
FEED_EXPORT_FIELDS = [
    'Name',
    'Scientific_Name',
    'Days_to_maturity',
    'Life_cycle',
    'Disease_resistance',
    'Hybrid_status',
    'image_urls',
    'Notes'
]
```

## Usage

### Running a Spider

**Basic command:**
```bash
py -m scrapy crawl johnnys
```

**Export to CSV (command line method):**
```bash
py -m scrapy crawl johnnys -o 2026SpringBuy.csv
```

**Export to multiple formats:**
```bash
py -m scrapy crawl johnnys -o 2026SpringBuy.csv -o 2026SpringBuy.json
```

### Creating a New Spider

1. **Generate spider template:**
   ```bash
   py -m scrapy genspider spider_name domain.com
   ```

2. **Edit the spider file** in `SeedInfo/spiders/`

3. **Run the spider** using the commands above

## Example Spider

The `johnnys.py` demonstrates scraping product information from Johnny's Seeds:

```python
import scrapy

class JohnnysSpider(scrapy.Spider):
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
    
    def parse(self, response):
        # Extract product title
        title = response.css('h1.product-name::text').get()
        subtitle = response.css('span.product-alternate-name::text').get()
        full_title = f"{title.strip()} {subtitle.strip()}" if title and subtitle else None
        
        # Extract facts from definition list
        facts_dl = response.css('dl.c-facts__list')[0]
        facts_dict = {}
        
        dt_elements = facts_dl.css('dt')
        dd_elements = facts_dl.css('dd')
        
        for dt, dd in zip(dt_elements, dd_elements):
            term = dt.css('h3::text').get()
            defn = dd.css('h4::text').get()
            
            # Handle multiple format definitions
            if not defn or defn.strip() in [',', '']:
                defn = ', '.join(dd.css('abbr::text').getall())
            
            if not defn or not defn.strip():
                defn = ' '.join(dd.css('::text').getall()).strip()
            
            if term and defn:
                facts_dict[term.strip()] = defn.strip()
        
        # Yield structured data
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
```

## Common Issues and Solutions

### File Access Errors

**Problem:** `FileSystemException: The process cannot access the file because it is being used by another process`

**Solution:**
- Close the CSV file in Excel or any text editor
- Close the file in PyCharm if open in the editor
- Use `overwrite: True` in settings.py to automatically handle file overwrites
- If needed, check Task Manager and end any stuck Excel processes

### Deleting Output Files

**Manual deletion (before running spider):**

Windows:
```bash
del output_filename.csv
scrapy crawl spider_name
```

Mac/Linux:
```bash
rm output_filename.csv
scrapy crawl spider_name
```

**Automatic deletion (in spider):**
```python
import os

class YourSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if os.path.exists('output_filename.csv'):
            os.remove('output_filename.csv')
```

### Python/pip Not Recognized

Use the `py -m` prefix for all commands:
```bash
py -m pip install package_name
py -m scrapy crawl spider_name
```

## Testing in Scrapy Shell

Test CSS selectors before adding them to your spider:

```bash
py -m scrapy shell "https://example.com/product-page"
```

In the shell:
```python
# Test selectors
response.css('h1.product-name::text').get()
response.css('dl.c-facts__list dt h3::text').getall()

# Test data extraction logic
facts_dl = response.css('dl.c-facts__list')[0]
dt_elements = facts_dl.css('dt')
dd_elements = facts_dl.css('dd')
```

## Data Output Format

CSV files contain the following columns:
- **name**: Product name and variety
- **scientific_name**: Botanical/scientific name
- **days_to_maturity**: Expected growing time
- **life_cycle**: Annual, biennial, or perennial
- **disease_resistance**: Disease resistance codes
- **hybrid_status**: Whether the variety is hybrid or open-pollinated
- **image_urls**: URL of the germination temp image
- **notes**: anything in culture section that need to be added

## Future Enhancements

- [ ] Add spiders for additional seed companies
- [ ] Implement pagination handling for catalog pages
- [ ] Add price tracking
- [ ] Create data validation pipelines
- [ ] Add automatic duplicate detection
- [ ] Implement scheduling for regular updates

## Notes

- This project was created for personal gardening research and reference
- All scraped data should respect website terms of service and robots.txt
- CSV files are automatically overwritten with each run when `overwrite: True` is set

## License

This project is for personal use.

## Author
Ashley Hunter
- Created for seed catalog research and gardening planning in Zone 7a, Oklahoma.
