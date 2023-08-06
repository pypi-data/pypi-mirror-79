"""Abstraction around a francophone school district school"""


class FSDSchool:
    """Abstraction around school-specific data parsed from the school
    district's website"""
    SCHOOL_FIELD = "Nom de l'école"
    OPEN_FIELD = "École"
    BUS_FIELD = "Autobus"
    MESSAGE_FIELD = "Messages"

    def __init__(self, df):
        """
        Args:
            df: Panda's dataframe containing school data parsed from the website
        """
        self._df = df

    def __str__(self):
        return self._df.to_markdown()

    def __repr__(self):
        return str(self)

    @property
    def name(self):
        """str: name of the school"""
        return self._df[self.SCHOOL_FIELD]

    @property
    def messages(self):
        """str: status messages associated with the school"""
        return self._df[self.MESSAGE_FIELD]

    @property
    def is_open(self):
        """bool: True if school is open, False if not"""
        return self._df[FSDSchool.OPEN_FIELD] == "Ouvert"

    @property
    def has_late_busses(self):
        """bool: True if 1 or more buses are late, False if all are running
        on time"""
        return self._df[FSDSchool.BUS_FIELD] != "À l’heure"
