from bs4.element import *
from datetime import datetime, timedelta, date
import pandas as pd


def date_arithmetics(start_date, durations, mode = 'addition'):
    parsed_start_date = datetime.strptime(start_date, "%d-%m-%Y")
    
    if mode.lower() == 'subtraction':
        pass
    elif mode.lower() == 'multiplication':
        pass
    elif mode.lower() == 'division':
        pass
    else:
        return (parsed_start_date + timedelta(days = durations)).strftime("%d-%m-%Y")

def get_hotel_geo_id_based_on_location(location):
    hotel_geo_data = pd.read_csv("C:/Projects/Python/DataScience/data/traveloka/traveloka hotel geo data.csv")
    return hotel_geo_data.set_index("location").loc[location]["hotel_geo_id"]

def check_input_date_in_one_year_ahead_range(today_date, check_in_date):
    one_year_ahead_date = today_date.replace(year = today_date.year + 1)

    if today_date <= check_in_date <= one_year_ahead_date:
        return True

    return False

def diff_month(today_date, check_in_date):
    diff_year = check_in_date.year - today_date.year

    if diff_year == 0:
        return check_in_date.month - today_date.month
    else:
        return 12 - today_date.month + check_in_date.month
    
def define_the_month_index_of_check_in_date_on_the_date_picker(check_in_date):
    today_date = date.today()
    
    if check_input_date_in_one_year_ahead_range(today_date, check_in_date):
        return diff_month(today_date, check_in_date) + 1
    else:
        raise Exception("")

def define_hotel_rating_and_reviewers(hotels):
    ratings = []
    reviewers = []
    for hotel in hotels:
        sibling = hotel.parent.find_next_sibling('div')
        if sibling == None:
            ratings.append(0)
            reviewers.append(0)
        else:
            rating_and_reviewers = sibling.find("div", class_ = "css-901oao r-t1w4ow r-1b43r93 r-b88u0q r-rjixqe r-fdjqy7").text
            ratings.append(define_rating(rating_and_reviewers))
            reviewers.append(define_reviewers(rating_and_reviewers))

    return ratings, reviewers

def define_rating(rating_and_reviewers):
    return float(rating_and_reviewers[0:rating_and_reviewers.index("(")])

def define_reviewers(rating_and_reviewers):
    reviewers = rating_and_reviewers[rating_and_reviewers.index("(") + 1 : rating_and_reviewers.index(")")]
    if "K" not in reviewers:
        return int(reviewers[:-7])

    return int(float(reviewers[0:reviewers.index("K")]) * 1000)
    
def reformat_price(prices):
    reformatted_prices = []
    for price in prices:
        temp_price = price.text
        temp_price = temp_price.replace("VND", "")
        temp_price = temp_price.replace(".", "")
        reformatted_prices.append(int(temp_price))
    return reformatted_prices