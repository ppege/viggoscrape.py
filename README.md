# Viggoscrape.py

Python library for scraping *[Viggo](http://viggo.dk/)* assignments by interacting with the [Viggoscrape API](https://api.nangurepo.com/v2/scrape).

>The API is designed for **danish** users, and time will be adjusted to the **CET** timezone.

## Quickstart

### Syntax

Viggoscrape.py uses the following syntax:
1. Provide subdomain, username and password on class initialization
2. Provide optional parameters: date, grouping mode and API version after initialization
3. Retrieve a list of assignments using the `get_assignments` method, or retrieve a
dictionary of assignment attributes using the `get_attributes` method.

### Usage example

Most of the time you'll want to do something like this:

#### 

```python
from viggoscrape import Viggoscrape

v = Viggoscrape(
    subdomain="example-subdomain",
    username="viggouser@gmail.com",
    password="password123456"
) # initialization
v.date = "2021-03-14" # get assignments within 2 weeks of this date

print(v.get_assignments()) # get a list of dictionaries representing assignments

```

The output should look something like this:
```json
[
    {
        "author": "14. mar 2021 11:09 by Teacher McTeacher",
        "date": "Monday 16. Mar",
        "description": "Read this and that blablabla, here are some links: https://github.com/nangurepo/ https://viggoscrape.xyz/",
        "subject": "History",
        "time": "10:45 - 11:30",
        "url": "https://subdomain-example.viggo.dk/Basic/HomeworkAndAssignment/Details/1234/#modal"
    },
    {
        "author": "17. mar 2021 18:09 by Other Teacher",
        "date": "Tuesday 20. Mar",
        "description": "Read page 170-200 of 'To kill a mockingbird'",
        "subject": "English",
        "time": "12:00 - 12:45",
        "url": "https://subdomain-example.viggo.dk/Basic/HomeworkAndAssignment/Details/5678/#modal"
    }
]
```
Swap out `v.get_assignments()` for `v.get_attributes()` and it'll look like this:

```json
{
    "subject": ["History", "English"],
    "date": ["Monday 16. Mar", "Tuesday 20. Mar"],
    "description": ["Read this and that blablabla, here are some links: https://github.com/nangurepo/ https://viggoscrape.xyz/", "Read page 170-200 of 'To kill a mockingbird'"],
    "author": ["14. mar 2021 11:09 by Teacher McTeacher", "17. mar 2021 18:09 by Other Teacher"],
    "url": ["https://subdomain-example.viggo.dk/Basic/HomeworkAndAssignment/Details/1234/#modal", "https://subdomain-example.viggo.dk/Basic/HomeworkAndAssignment/Details/5678/#modal"]
}
```
This can be used for other purposes.

Do note that if you, for some reason, need to use v1 of the API, data will always be returned as a dictionary of attributes, with the addition of file names and urls. Version 1 of the API uses a more thorough scan, scraping each individual assignment page, carrying a huge sacrifice of efficiency.

