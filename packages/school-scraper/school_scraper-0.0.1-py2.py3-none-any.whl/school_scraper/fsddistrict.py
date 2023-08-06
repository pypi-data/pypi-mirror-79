"""Primitives for reading francophone school district information"""
from .fsdschool import FSDSchool


class FSDDistrict:
    """Abstraction around school district data parsed from the district website
    """
    DISTRICT_FIELD = "Région"

    def __init__(self, df):
        """
        Args:
            df: Pandas data frame describing the district
        """
        self._df = df

    def __str__(self):
        return self._df.to_markdown()

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        """str: Name of the district"""
        # NOTE: Some districts have the same name but in different character
        #       casing so we just return a lower-cased representation
        temp = self._df[self.DISTRICT_FIELD].str.lower().unique()
        assert len(temp) == 1
        return temp[0]

    @property
    def schools(self):
        """list (FSDSchool): 1 or more schools associated with this district"""
        return [FSDSchool(df[1]) for df in self._df.iterrows()]

    @property
    def school_names(self):
        """list (str): list of school names associated with this district"""
        retval = list()
        for cur_school in self.schools:
            retval.append(cur_school.name)
        return retval

    def get_school(self, name):
        """Gets a specific school from the district

        Args:
            name (str):
                name of the school to get data for

        Returns:
            FSDSchool:
                reference to the school with the given name, or None if no
                such school exists
        """
        for cur_school in self.schools:
            if cur_school.name.lower() == name.lower():
                return cur_school
        return None
