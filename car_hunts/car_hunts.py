from datetime import datetime, timedelta
from dataclasses import dataclass

DATE_FORMAT = "%d.%m.%Y"


@dataclass
class Car:
    name: str
    dates: [datetime]
    next_hunt: datetime = datetime.today()
    avg_weeks: int = 0


def main():
    dictionary = {}
    parse_input(dictionary)

    cars_due = []
    cars_upcoming = []
    cars_once = []
    sort_data(cars_due, cars_once, cars_upcoming, dictionary)
    create_output(cars_due, cars_once, cars_upcoming)


def parse_input(dictionary):
    with open("car_hunts.csv", "r") as csv_file:
        for line in csv_file:
            elements = list(filter(lambda x: x != "", line.strip('\n').split(";")))
            date = datetime.strptime(elements[0], DATE_FORMAT)
            for car_name in elements[1:]:
                if car_name in dictionary:
                    dictionary[car_name].dates.append(date)
                else:
                    dictionary[car_name] = Car(car_name, [date])


def sort_data(cars_due, cars_once, cars_upcoming, dictionary):
    for car_name, car in sorted(dictionary.items()):
        if len(car.dates) > 1:
            durations = 0
            for i in range(len(car.dates) - 1):
                days = abs((car.dates[i] - car.dates[i + 1]).days)
                durations += (days / 7)

            car.avg_weeks = int(durations / (len(car.dates) - 1))
            car.next_hunt = car.dates[-1] + timedelta(weeks=car.avg_weeks)

            if car.next_hunt < datetime.today():
                cars_due.append(car)
            else:
                cars_upcoming.append(car)
        else:
            cars_once.append(car)


def create_output(cars_due, cars_once, cars_upcoming):
    print("----------Appeared once----------")
    print(f"{'Car Name' : <30}{'' : ^10}{'Date' : >15}")
    for car in sorted(cars_once, key=lambda x: x.dates[0]):
        print(f"{car.name : <30}{'': ^10}{car.dates[0].strftime(DATE_FORMAT) : >15}")

    print()
    print("----------Upcoming----------")
    print(f"{'Car Name' : <30}{'AVG Weeks' : ^10}{'Next Date' : >15}")
    for car in sorted(cars_upcoming, key=lambda x: x.next_hunt):
        print(f"{car.name : <30}{car.avg_weeks : ^10}{car.next_hunt.strftime(DATE_FORMAT) : >15}")

    print()
    print("----------Due----------")
    print(f"{'Car Name' : <30}{'AVG Weeks' : ^10}{'Next Date' : >15}")
    for car in sorted(cars_due, key=lambda x: x.next_hunt):
        print(f"{car.name : <30}{car.avg_weeks : ^10}{car.next_hunt.strftime(DATE_FORMAT) : >15}")


if __name__ == '__main__':
    main()
