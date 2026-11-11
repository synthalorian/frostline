# frostline

Offline planting windows from a bundled frost-date table.

Dates are planning estimates, not NOAA-certified forecasts.

Author: synthalorian

## Build

No build step. Python 3 standard library only. Nothing to install, and the tool does not use the network.

## Test

```sh
python -m unittest discover -s tests
```

## Usage

```sh
python -m frostline window --city Richmond --crop tomato
```

```
city: Richmond
crop: tomato
sow: 03-04
transplant: 04-15
```

City and crop names match case-insensitively. Sow is last spring frost minus the crop's sow days. Transplant is last spring frost plus the crop's transplant days. A negative transplant offset is that many days before last spring frost. Dates print as MM-DD. Month-day math uses reference year 2026, which is not a leap year.

Cities whose frost fields are `00-00` print `no frost date on file` and exit 0. An unknown city or crop writes a message to stderr and exits 2.
