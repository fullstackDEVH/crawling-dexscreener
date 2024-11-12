from celery import Celery
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from celery.utils.log import get_task_logger
import time
from selenium import webdriver
from celery.schedules import crontab
from selenium_stealth import stealth


logger = get_task_logger(__name__)


# Initialize Celery and set the broker (Redis URL defined in the Docker Compose file)
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Define a simple Celery task
@celery_app.task
def run_browser():
    logger.info('Start crawling')

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # Optional: Comment out if you want a visible browser for testing
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Initialize undetected ChromeDriver
    logger.info('Add options')
    driver = uc.Chrome(options=options)

    # Open the target URL
    url = "https://dexscreener.com/ethereum?rankBy=trendingScoreH24&order=desc"
    driver.get(url)

    # Optional: Allow time for any security checks
    time.sleep(10)

    container = driver.find_element(By.CSS_SELECTOR, '.ds-dex-table.ds-dex-table-top')
    
    rows = []

    if container :
        table_rows = container.find_elements(By.CSS_SELECTOR, '.ds-dex-table-row.ds-dex-table-row-top')

        for row in table_rows:
            rank = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-badge-pair-no").text
            dex_name = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-token img.ds-dex-table-row-dex-icon").get_attribute("title")
            token_name = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-base-token-symbol").text
            pair = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-quote-token-symbol").text
            token_full_name = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-base-token-name-text").text
            # boost_value = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-base-token-name-boosts").text
            price = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-price").text
            pair_age = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-pair-age span").text
            txns = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-txns").text
            volume = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-volume").text
            makers = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-makers").text
            price_change_m5 = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-price-change-m5 span").text
            price_change_h1 = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-price-change-h1 span").text
            price_change_h6 = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-price-change-h6 span").text
            price_change_h24 = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-price-change-h24 span").text
            liquidity = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-liquidity").text
            market_cap = row.find_element(By.CSS_SELECTOR, ".ds-dex-table-row-col-market-cap").text

            rows.append({
                "Rank": rank,
                "DEX Name": dex_name,
                "Token Name": token_name,
                "Pair": pair,
                "Token Full Name": token_full_name,
                # "Boost Value": boost_value,
                "Price": price,
                "Pair Age": pair_age,
                "Transactions": txns,
                "Volume": volume,
                "Makers": makers,
                "Price Change (5m)": price_change_m5,
                "Price Change (1h)": price_change_h1,
                "Price Change (6h)": price_change_h6,
                "Price Change (24h)": price_change_h24,
                "Liquidity": liquidity,
                "Market Cap": market_cap
            })
    else : 
        print("Table with class 'ds-dex-table ds-dex-table-top' was not found.")

    driver.quit()
    return "Completed"


# Configure periodic task schedule (every minute)
celery_app.conf.beat_schedule = {
    'run-my-periodic-task-every-minute': {
        'task': 'dexscreener_crawling.dexscreener_crawling.tasks.run_browser',
        'schedule': crontab(minute="*"),  
    },
}

