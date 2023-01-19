# Booking Hotels Ranking

## Introduction

### Purpose

This project is a machine learning project to predict hotels's rooms prices of [Booking.com](https://www.booking.com/en-gb/) in order to help the consumer in his choices.

Tourism industry is very volatile in terms of prices whether on the destination or the period of the year. Thus, we wanted to express rooms prices' factors with a consumer approach such with a given destination at a given date, the model was able to tell wheter an hotel room is a good (or not) characteritics/price ratio compared the competition at this destination for the same date. The idea is to predict the hotel room's price depending on its characteristics with a model trained on competitors hotels and then to compare this predicted price on the real price given by Booking. If the ratio is positive which means the price predicted by the model is lower than the real price on Booking, we could admit this room is at a low price given its characteristics. The output was to build an app for consumers usage with objectives to compare several hotels' rooms in order to

### Method

1. Data collection from [Booking.com](https://www.booking.com/en-gb/) on destination and period choose by consumer.
2. Data cleaning and preprocessing to get a dataset ready for machine learning.
3. Models training and hyperparameters optimisation
4. Best model selection and comparison of true values to predicted values.

## Data collection using Web Scraping

The `scraping.py` file is executed in command lines using 2 parameters :

- destination
- checkin_date

Example with `python -m scraping.py Paris 15 January 2023`

![Alt Text](.gif)

The json dataset `Booking_Hotels.json` obtained from `scraping.py` is such :

| Variable            | Type  | Description                                            |
| ------------------- | ----- | ------------------------------------------------------ |
| `Room_id`           | str   | Room's option ID number                                |
| `Room_name`         | str   | Room name                                              |
| `Room_price`        | int   | Room price for selected duration                       |
| `Room_sleeps`       | int   | Room's option total occupancy                          |
| `Room_promo`        | str   | Room price promotion (square meters)                   |
| `Room_breakfast`    | str   | Room's option information about breakfast              |
| `Room_cancellation` | str   | Room's option information about cancellation           |
| `Room_prepayment`   | str   | Room's option information about prepayment             |
| `Room_size`         | int   | Room's option size (square meters)                     |
| `Hotel_id`          | str   | Hotel id                                               |
| `Hotel_name`        | str   | Hotel name                                             |
| `Hotel_address`     | str   | Hotel address                                          |
| `Hotel_grade`       | float | Hotel's booking grade by consumers                     |
| `Hotel_type`        | str   | Property type (hotel, apartement, guest house ...)     |
| `Hotel_nb_reviews`  | int   | Hotel's number of consumers' reviews                   |
| `Hotel_facilities`  | dict  | Hotel's facilities                                     |
| `Hotel_stars`       | int   | Hotel's number stars                                   |
| `Hotel_categories`  | dict  | Hotel's grades category (Staff, Comfort, Location ...) |

## Data preprocessing

## Descriptive statistics

Our target variable `Room_prices` distribution :

![Prix](img/capture_density.png)

Note we have a skew normal distribution with the average price $\approx$ 287€ higher than the median price $\approx$ 250€.

## Machine Learning

## Conclusion

### Next steps to implement

- Automation
