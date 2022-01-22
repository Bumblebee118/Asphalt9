# Car Hunts

This script parses the [car_hunts.csv](car_hunts.csv) file, which contains all dates for car hunts since 2020. The data mainly originates from this [reddit post](https://www.reddit.com/r/Asphalt9/comments/orzt24/car_hunt_history/). 
The script calculates the average amount of weeks between the hunts for a car. If there has been only one hunt up to this date, The car is listed in the *Appeared once* section of the output. Furthermore, it lists the approximate date when the car should appear again in a hunt, due to the previously calculated average occurences.
If this date lies in the past, the car is listed in the *Due* section of the output.
