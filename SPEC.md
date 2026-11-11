# frostline

Python 3 stdlib only. No network. Dates are planning estimates, not NOAA-certified forecasts. Say that in the README.

## Test command

`python -m unittest discover -s tests`

## Data

Ship `data/cities.csv` and `data/crops.csv` exactly as follows.

cities.csv header: `city,last_spring,first_fall`

```
Richmond,04-15,10-26
Minneapolis,05-15,09-30
Atlanta,03-24,11-08
Portland,04-03,11-15
Phoenix,01-15,12-15
Denver,05-05,10-07
Chicago,04-20,10-21
Miami,00-00,00-00
Seattle,03-24,11-11
Austin,03-01,11-28
Boston,04-08,11-07
Nashville,04-06,10-31
Dallas,03-18,11-20
Detroit,04-26,10-20
Kansas City,04-15,10-20
San Francisco,01-15,12-15
Albuquerque,04-16,10-28
Fargo,05-15,09-24
Honolulu,00-00,00-00
Anchorage,05-18,09-15
```

crops.csv header: `crop,sow_days_before_last_frost,transplant_days_after_last_frost`

```
tomato,42,0
lettuce,14,-14
beans,0,7
basil,28,7
```

Negative transplant days means that many days before last spring frost.

## Command

`frostline window --city Richmond --crop tomato`

Reference year for month-day math is 2026 (not a leap year). Match city and crop case-insensitively.

If the city frost fields are `00-00`, print `no frost date on file` and exit 0.

Otherwise print exactly these four lines, dates as MM-DD:

```
city: Richmond
crop: tomato
sow: 03-04
transplant: 04-15
```

sow = last_spring minus sow_days_before_last_frost.
transplant = last_spring plus transplant_days_after_last_frost.

Unknown city or crop: stderr message, exit 2.

## Tests

Richmond tomato is sow 03-04, transplant 04-15. Lettuce transplant is 04-01. Miami prints the no-frost line. Unknown city exits 2.
