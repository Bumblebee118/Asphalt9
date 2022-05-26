"""This module analyzes the past car hunts and tries to give a prediction for future car hunts.
"""

from datetime import datetime, timedelta
import pandas as pd

DATE_FORMAT = "%d.%m.%Y"

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def main():
    """Main method that calls all the sub-methods.
    """
    dataframe = parse_input()

    cars_due = {}
    cars_upcoming = {}
    cars_once = {}
    sort_data(cars_due, cars_once, cars_upcoming, dataframe)
    print(pd.DataFrame(cars_once).transpose().sort_values(by=0)
          .rename(columns={0: "Last Occurrence"}))
    print()
    print(pd.DataFrame(cars_upcoming).transpose().sort_values(by=1)
          .rename(columns={0: "Avg Weeks", 1: "Next Occurrence"}))
    print()
    print(pd.DataFrame(cars_due).transpose().sort_values(by=1)
          .rename(columns={0: "Avg Weeks", 1: "Supposed Occurrence"}))


def parse_input() -> pd.DataFrame:
    """Parses the csv file and creates an entry in the dictionary for every car that had a hunt
    with the according Car object as a value.

    :rtype: The dataframe with all the cars and their dates
    """
    dataframe = pd.read_csv("car_hunts.csv").fillna("")
    cars = set(dataframe["Car1"].unique())
    cars.update(set(dataframe["Car2"].unique()))
    cars.update(set(dataframe["Car3"].unique()))
    cars.remove("")
    cars = list(cars)
    dictionary = {}
    for car in cars:
        occurrences = list(dataframe[dataframe["Car1"] == car].index.values)
        occurrences.extend(x for x in dataframe[dataframe["Car2"] == car].index.values)
        occurrences.extend(x for x in dataframe[dataframe["Car3"] == car].index.values)
        occurrences.sort()
        dictionary[car] = [datetime.strptime(dataframe.iloc[x].Date, DATE_FORMAT)
                           for x in occurrences]
    return pd.DataFrame.from_dict(dictionary, orient='index')


def sort_data(cars_due, cars_once, cars_upcoming, dataframe):
    """Sorts the cars into the three categories.

    :param cars_due: List of all cars that should have had a hunt already.
    :param cars_once: List of all cars that had only one hunt.
    :param cars_upcoming: List of all cars that will probably have a hunt in the future and the
    approximate date can be calculated.
    :param dataframe: The dataframe containing all the cars.
    """
    for row in dataframe.itertuples():
        last_date_idx = [idx for idx, val in reversed(list(enumerate(row))) if val is not
                         pd.NaT][0]
        if last_date_idx > 1:  # This means only one date is in the dataframe
            durations = 0
            for i in range(1, last_date_idx):
                days = abs((row[i] - row[i + 1]).days)
                durations += (days / 7)

            avg_weeks = int(durations / (last_date_idx - 1))
            next_hunt = row[last_date_idx] + timedelta(weeks=avg_weeks)

            if next_hunt < datetime.today():
                cars_due[row[0]] = [avg_weeks, next_hunt]
            else:
                cars_upcoming[row[0]] = [avg_weeks, next_hunt]
        else:
            cars_once[row[0]] = [row[1]]


if __name__ == '__main__':
    main()
