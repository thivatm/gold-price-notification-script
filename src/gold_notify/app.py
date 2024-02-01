import requests
import telebot
import json
import os

from bs4 import BeautifulSoup
from datetime import datetime

telebotKey = os.environ['TELEBOT_KEY']

def lambda_handler(event, context):

    bot = telebot.TeleBot(telebotKey)
    # Params
    url = 'https://www.ravijewellers.lk/'
    tag = 'h5'
    element_class = 'gold_title'
    updated_on = get_date(url)
    updated_date = datetime.strptime(updated_on, "%d %b, %Y").date()

    # Initital date set
    initial_date = updated_on

    new_updated_date = get_date(url)
    new_date = datetime.strptime(new_updated_date, "%d %b, %Y").date()

    # Execute
    value = scrape_element_value(url, tag, element_class, new_date)
    initial_value = value
    new_value = ''

    if initial_value != new_value:
        # Send to bot
        bot.send_message("@goldratelk", value, parse_mode="markdown")
        new_value = value

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Script executed successfully!",
        }),
    }


def get_date(url):
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get Date 
    div = soup.find('div', class_='gold_rate_box')
    p_tag = div.find('p')
    updated_on = p_tag.text.strip().split('Updated on ')[-1]

    return updated_on

def scrape_element_value(url, tag, element_class, updated_on):
    # Fetch the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get title
    message_title = f"*Gold Price Today* \nLast Updated: {updated_on}\n"

    # Find the specific gold_title class
    values = ""
    gold_titles = soup.find_all(tag, class_=element_class)
    if gold_titles:
        for gold_title in gold_titles:
            # Get the next sibling element (which is the <h3> tag)
            h3_tag = gold_title.find_next_sibling('h3')
            if h3_tag:
                value = h3_tag.get_text()
                values += f"🔸 *{gold_title.get_text()}*: {value} LKR per pavan\n"
            else:
                print(gold_title.get_text(), " NOT_FOUND")
    else:
        print("NOT_FOUND")

    main_message = f'{message_title}\n{values}'
    print(main_message)

    return main_message

