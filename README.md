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

The first two items are obvious, but what is a fingerprint?



```python
from viggoscrape.scraper import get_assignments
assignment_data = scan("subdomain-example", {
    "UserName": "example@example.com",
    "Password": "Password1234",
    "fingerprint": "ViggoLog=f8f567-19t7-5hg7-d68n-and85mba2"
})
```