# Turris Timezone

Due to missing /usr/share/zoneinfo on OpenWRT this package should provide some
basic data extracted from /usr/share/zoneinfo of build machnine.

Currently it contains:

* `TZ_GNU` - mapping between timezone name and GNU timezone representation
	see https://docs.python.org/3/library/time.html#time.tzset
	see https://man7.org/linux/man-pages/man3/tzset.3.html

* `COUNTRIES` - mapping between country ISO code (2 letters) and English name of the country
	see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements

## Installation

```bash
pip install .
```

## Usage
```
>>> import turris_timezone
>>> turris_timezone.TZ_GNU.get("Europe/Prague")
'CET-1CEST,M3.5.0,M10.5.0/3'
>>> turris_timezone.COUNTRIES.get("CZ")
'Czechia'
```
