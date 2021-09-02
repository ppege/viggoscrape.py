# Viggoscrape

Python library for scraping *[Viggo](http://viggo.dk/)* assignments.

>This library is designed for **danish** users, and time will be adjusted to the **CET** timezone.

## Quickstart

### Information syntax

To use Viggoscrape, you need to provide it with login info and a subdomain.

#### Subdomain

For your subdomain, specify only the subdomain, like this:

`subdomain-example`

And not like this:

`subdomain-example.viggo.dk`

#### Login info

The login info uses 3 pieces of information:
-  Username
-  Password
-  Fingerprint

The first two items are obvious.
But to find your fingerprint, you'll need to look through the html of your login page's source code, and look for a `ViggoLog=x` value.

#### Usage example

Let's try this out! We'll import the library, give it the required info and print the resulting dictionary.

```python
from viggoscrape.scraper import get_assignments
subdomain = "subdomain-example"
login_info = {
    "USERNAME": "example@example.com",
    "PASSWORD": "Password1234",
    "FINGERPRINT": "ViggoLog=f8f567-19t7-5hg7-d68n-and85mba2"
}
assignment_data = get_assignments(subdomain, login_info)
print(assignment_data)
```

Our output would look something like this:
```json
{
    "subject": ["English", "Math"],
    "time": ["31. aug 12:00", "2. sep 08:55"],
    "description": ["Read pages 30 and 31", "Finish A, B and C"],
    "author": ["28. aug 11:25 by John Doe", "31. aug 15:30 by Peter Anker"],
    "files": ["None", "example.com/algebra.pdf"],
    "file_names": ["None", "Intro to algebra"],
    "url": ["https://example-subdomain.viggo.dk/Basic/HomewordAndAssignment/Details/1234/#modal", "https://example-subdomain.viggo.dk/Basic/HomewordAndAssignment/Details/1235/#modal"]
}
```

Now, you can do anything you want with this newfound data, like save it to a json file, create an embed for your [discord bot](https://github.com/nangurepo/fessor), or any other purpose. Just use the same index on all lists and the data should match.