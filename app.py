from flask import Flask, render_template
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def check_airbnb():
    today = datetime.today()
    reserved_dates = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto("https://www.airbnb.co.kr/rooms/1315132686200650033#availability-calendar")
        page.wait_for_timeout(5000)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()

        soup = BeautifulSoup(html, "html.parser")
        reserved_tags = soup.find_all(attrs={"data-is-day-blocked": "true"})

        for tag in reserved_tags:
            test_id = tag.get("data-testid", "")
            if test_id.startswith("calendar-day-"):
                date_str = test_id.replace("calendar-day-", "").strip(".")
                try:
                    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                    if date_obj > today:
                        reserved_dates.append(date_str)
                except:
                    continue

    return render_template("index.html", dates=sorted(set(reserved_dates)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
