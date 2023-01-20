# Booking Hotels Ranking

## Introduction

### Objectives

This project is a machine learning project to predict hotels's rooms prices of [Booking.com](https://www.booking.com/en-gb/) in order to help the consumer in his choices.

Tourism industry is very volatile in terms of prices whether on the destination or the period of the year. Thus, we wanted to express rooms prices' factors with a consumer approach such with a given destination at a given date, the model was able to tell wheter an hotel room is a good (or not) characteritics/price ratio compared the competition at this destination for the same date. The idea is to predict the hotel room's price depending on its characteristics with a model trained on competitors hotels and then to compare this predicted price on the real price given by Booking. If the ratio is positive which means the price predicted by the model is higher than the real price on Booking, we could admit this room is at a low price given its characteristics. The output was to build an app for consumer usage which would compare several hotels' rooms choosed to concurrency at the same destination for the same time period.

### Method

**Application's steps** :
1. Data collection from [Booking.com](https://www.booking.com/en-gb/) on stayed placed `{destination}` and period choose by consumer `{checkin_date}`.
2. Data cleaning and preprocessing to get a dataset ready for machine learning.
3. Models training with hyperparameters optimization, best model selection and comparison of true values to predicted values on given rooms `{room_to_rank}`.

**Command lines launcher** :
 - `py -m main.py {destination} {checkin_date} {room_to_rank}`

## Data collection using Web Scraping

The `scraping.py` file is executed in `main.py` using 2 arguments :

- *destination*
- *checkin_date*

During our entire project, as an example, we choose "Paris" for destination and "15 January 2023" for checkin date.

The app is launched using : `python -m main.py Paris 15 January 2023`

![Search](img/capture_search.png)

After initialazing Booking's reseach on arguments gave by user, the program naviguates through hotels found and its rooms.

## Descriptive statistics

The json dataset `Booking_Hotels.json` obtained from `scraping.py` is such :

| Variable            | Type  | Description                                            | NA  |
| ------------------- | ----- | ------------------------------------------------------ | ----|
| `Room_id`           | str   | Room's option ID number                                |  /  |
| `Room_name`         | str   | Room name                                              |  /  |
| `Room_price`        | int   | Room price for selected duration                       |  /  |
| `Room_sleeps`       | int   | Room's option total occupancy                          |  /  |
| `Room_promo`        | str   | Room price promotion (square meters)                   |  /  |
| `Room_breakfast`    | str   | Room's option information about breakfast              |  /  |
| `Room_cancellation` | str   | Room's option information about cancellation           |  /  |
| `Room_prepayment`   | str   | Room's option information about prepayment             |  /  |
| `Room_size`         | int   | Room's option size (square meters)                     | 323 |
| `Hotel_id`          | str   | Hotel id                                               |  /  |
| `Hotel_name`        | str   | Hotel name                                             |  /  |
| `Hotel_address`     | str   | Hotel address                                          |  /  |
| `Hotel_grade`       | float | Hotel's booking grade by consumers                     |  7  |
| `Hotel_type`        | str   | Property type (hotel, apartement, guest house ...)     |  /  |
| `Hotel_nb_reviews`  | int   | Hotel's number of consumers' reviews                   |  /  |
| `Hotel_facilities`  | dict  | Hotel's facilities                                     |  /  |
| `Hotel_stars`       | int   | Hotel's number stars                                   |  /  |
| `Hotel_categories`  | dict  | Hotel's grades category (Staff, Comfort, Location ...) |  /  |

Note we had missing values for some variables chosen for modelization :

![NA](img/capture_na.png)

Our target variable `Room_prices` distribution :

![Prix](img/capture_density.png)

Note we have a skew normal distribution with the average price $\approx$ 287€ higher than the median price $\approx$ 250€.

## Data preprocessing

The `preprocessing.py` file clean dataset obtained from web scraping by :
- Removing unexpected characters in str varibles.
- Creating new variables from variables obtained.
- Removing missing values with NaN.
- Converting variables types.
- Removing rooms which are not type "Hotel".
- Creating the final dataset for machine learning.

## Machine Learning

## Conclusion

### Next steps to implement

- Scraping tags' automation
- 
