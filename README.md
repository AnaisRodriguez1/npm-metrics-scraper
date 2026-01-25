# NPM Metrics Scraper

This is a Scrapy project designed to scrape key metrics for specified NPM packages.

---

### Core Workflow

The scraper executes a four-step process for each package in a predefined list.

1.  **Downloads API:** It queries the `api.npmjs.org` endpoint to get the **download count** for the last month.
2.  **Registry API:** It queries the `registry.npmjs.org` endpoint to fetch detailed **package metadata**, including:
    * Current version
    * Description (purpose)
    * Dependencies
    * License
    * Maintainer count
    * Unpacked size
    * Tarball URL
3.  **Local Code Analysis:** The `Pipeline` downloads the `.tgz` tarball, unzips it to a temporary folder, and analyzes the code to **count the total JS/TS files** and simulate a **function count** using AST.
4.  **Output:** All collected data is saved into `npm_metrics_results.json`.

---

### 🚀 Quick Start

1.  **Clone & Setup:**
    ```bash
    git clone [https://github.com/AnaisRodriguez1/npm-metrics-scraper.git](https://github.com/AnaisRodriguez1/npm-metrics-scraper.git)
    cd npm-metrics-scraper
    python -m venv .venv
    # Activate virtual environment
    # Windows: .\.venv\Scripts\Activate.ps1
    # Linux/Mac: source .venv/bin/activate
    ```

2.  **Install:**
    ```bash
    cd npm-metrics-package
    pip install -r requirements.txt
    ```

3.  **Run:**
    ```bash
    scrapy crawl package_info_spider -o npm_metrics_results.json
    ```

---

### Configuration

* **Change Packages:** Edit the `package_list` variable in `npm_metrics_package/spiders/package_info_spider.py`.
* **Rate Limiting:** Adjust `DOWNLOAD_DELAY` in `npm_metrics_package/settings.py` to avoid overloading the server.

## TODO

* **Refine AST Function Counting:** Filter out undeclared functions (e.g., anonymous callbacks) and scalability-related boilerplate to ensure the metric reflects only core business logic.
