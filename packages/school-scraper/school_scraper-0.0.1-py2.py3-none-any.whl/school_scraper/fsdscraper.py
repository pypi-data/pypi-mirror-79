"""Scraper  for New Brunswick francophone school district website"""
import logging
import requests
import pandas as pd
from .fsdschool import FSDSchool
from .fsddistrict import FSDDistrict


class FSDScraper:
    """Interface for parsing HTML data loaded from the New Brunswick
    francophone school district website"""

    SCHEDULE_URL = \
        "https://bp.nbed.nb.ca/notices/BPRFtbl.aspx?dst=dsfs&amp;vtbl=1"

    def __init__(self, html):
        """
        Args:
            html (str):
                HTML data loaded from the website. Is expected to contain a
                single HTML table containing rows describing each school in
                each school district
        """
        assert FSDScraper.validate(html)

        temp = pd.read_html(
            html, header=0, converters={FSDSchool.MESSAGE_FIELD: str})

        self._data = temp[0]
        self._data.fillna("", inplace=True)

    def __str__(self):
        return self._data.to_markdown()

    @staticmethod
    def validate(html):
        """Checks to see if HTML loaded from the website is parseable

        Args:
            html (str):
                HTML data loaded from the district website

        Returns:
            bool:
                True if the HTML content was parseable, False if not. Details
                of any parsing errors are reported to the logger.
        """
        log = logging.getLogger(__name__)
        try:
            temp = pd.read_html(
                html, header=0, converters={FSDSchool.MESSAGE_FIELD: str},
                flavor="lxml")
        except ValueError as err:
            log.error("Error parsing HTML input:")
            log.error(err)
            log.debug(html)
            return False

        if len(temp) != 1:
            log.error(f"Expected 1 HTML table in the source data but "
                      f"found {len(temp)} instead")
            return False
        data = temp[0]
        data.fillna("", inplace=True)

        log.debug("Parsed HTML data table:")
        log.debug(data.to_markdown())

        school_names = list()
        for cur_school in data[FSDSchool.SCHOOL_FIELD]:
            if cur_school == "":
                log.error("Detected row with no valid school name")
                return False

            if cur_school in school_names:
                log.error(f"Multiple schools with the same name "
                          f"detected: {cur_school}")
                return False
            school_names.append(cur_school)

        for cur_district in data[FSDDistrict.DISTRICT_FIELD]:
            if cur_district == "":
                log.error("Detected row with no valid district name")
                return False

        return True

    @property
    def districts(self):
        """list (FSDDistrict): 0 or more districts parsed from the HTML content
        """
        unique_names = self._data[FSDDistrict.DISTRICT_FIELD].str.lower().unique()
        retval = list()
        for cur_name in unique_names:
            rows = self._data[self._data[FSDDistrict.DISTRICT_FIELD].str.lower() == cur_name]
            retval.append(FSDDistrict(rows))
        return retval

    def get_district(self, name):
        """Gets a specific district from the HTML content

        Args:
            name (str):
                the name of the district to locate

        Returns:
            FSDDistrict:
                Reference to the district details for the named district, or
                None if no district with the given name exists
        """
        for cur_district in self.districts:
            if cur_district.name.lower() == name.lower():
                return cur_district
        return None

    @property
    def district_names(self):
        """list (str): list of names of all districts parsed from the HTML"""
        retval = list()
        for cur_district in self.districts:
            retval.append(cur_district.name)
        return retval

    @property
    def school_names(self):
        """list (str): list of unique names of all schools in all districts"""
        retval = list()
        for cur_district in self.districts:
            for cur_school in cur_district.schools:
                retval.append(cur_school.name)
        return retval


if __name__ == "__main__":  # pragma: no cover
    text = requests.get(FSDScraper.SCHEDULE_URL).text
    print(FSDScraper.validate(text))
    obj = FSDScraper(text)
    print(obj)
