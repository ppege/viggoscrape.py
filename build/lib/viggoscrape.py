"""Scans for assignments on viggo using requests."""
import requests

class Viggoscrape():
    """Handles input and gives the user options"""
    def __init__(
        self,
        username: str,
        password: str,
        subdomain: str
    ):
        """Construct"""
        self.version = "v2"
        self.date = "None"
        self.subdomain = subdomain
        self.username = username
        self.password = password

    def get_assignments(self) -> list:
        """Get the assignments from viggoscrape.xyz as a list"""
        return self._get_data(list)

    def get_attributes(self) -> dict:
        """Get the assignments from viggoscrape.xyz as a dictionary"""
        return self._get_data(dict)

    def _get_data(self, grouping) -> str:
        url = self._create_url(grouping=grouping)
        data = requests.get(url)
        return data.json()

    def _create_url(self, grouping) -> str:
        return ''.join(
            [
                'https://viggoscrape.xyz/api/',
                self.version,
                '/scrape?date=',
                self.date,
                '&groupByAssignment=',
                str(int(grouping==list)),
                '&subdomain=',
                self.subdomain,
                '&username=',
                self.username,
                '&password=',
                self.password
            ]
        )
