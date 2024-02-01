# Gold Price Tracker

This script fetches the latest gold prices from 'https://www.ravijewellers.lk/' and sends updates via a Telegram bot.

## Dependencies

- `requests`
- `telebot`
- `json`
- `os`
- `BeautifulSoup`
- `datetime`

## Environment Variables

- `TELEBOT_KEY`: Your Telegram bot key.

## Functions

- `lambda_handler(event, context)`: The main function that gets executed. It fetches the gold prices, compares them with the previous prices, and sends an update if there's a change.

- `get_date(url)`: Fetches the date when the gold prices were last updated from the website.

- `scrape_element_value(url, tag, element_class, updated_on)`: Scrapes the gold prices from the website.

## Usage

The script is designed to be used as an AWS Lambda function. However, you can also run it locally by calling the `lambda_handler` function.

Please note that you need to set the `TELEBOT_KEY` environment variable before running the script.
