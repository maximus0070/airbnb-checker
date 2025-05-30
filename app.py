from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time

app = Flask(__name__)

@app.route("/")
def check_airbnb():
    url = "https://www.airbnb.co.kr/rooms/1315132686200650033#availability-calendar"
    today = datetime.today()

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=ko-KR')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    reserved_tags = soup.find_all(attrs={"data-is-day-blocked": "true"})

    reserved_dates = []
    for tag in reserved_tags:
        test_id = tag.get("data-testid", "")
        if test_id and test_id.startswith("calendar-day-"):
            date_str = test_id.replace("calendar-day-", "").strip(".")
            try:
                date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                if date_obj > today:
                    reserved_dates.append(date_str)
            except ValueError:
                continue

    return render_template("index.html", dates=sorted(set(reserved_dates)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

