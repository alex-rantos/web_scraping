""" Script extracting information from stackoverflow questions feed and inserting them to a postgres database """
from db_interface import PostgresDB
import requests
from bs4 import BeautifulSoup
import sys

if __name__ == "__main__":
    db = PostgresDB()
    pages = 10
    if len(sys.argv) == 2:
        if sys.argv[1].isdigit:
            pages = sys.argv[1]
    for i in range(pages):

        response = requests.get(
            "https://stackoverflow.com/questions?tab=newest&page=" + str(i+1))
        soup = BeautifulSoup(response.text, "html.parser")

        questions = soup.select(".question-summary")
        for q in questions:
            href = q.select_one(".summary h3 a")['href']
            title = q.select_one(".question-hyperlink").getText()
            user = q.select_one("div.user-details a").getText()
            likes = q.select_one(
                "span.vote-count-post strong").getText()
            views = q.select_one("div.views").getText().strip().split(" ")[0]
            tags = q.select("a.post-tag")
            tags_array = []
            for tag in tags:
                tags_array.append(tag.getText())
            tags = "||".join(tags_array)
            params = (href, title, user, likes, views, tags,)
            db.insert_into(params)
            print(params)
