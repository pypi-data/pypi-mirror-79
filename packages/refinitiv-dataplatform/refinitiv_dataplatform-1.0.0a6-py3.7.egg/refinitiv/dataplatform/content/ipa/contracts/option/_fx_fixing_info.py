# coding: utf8


__all__ = ["FxFixingInfo"]

from ...enum_types.fixing_frequency import FixingFrequency
from ._abstracted_class import FixingInfo


class FxFixingInfo(FixingInfo):
    def __init__(
            self,
            fixing_frequency=None,
            fixing_ric_source=None,
            fixing_start_date=None,
            include_holidays=None,
            include_weekends=None
    ):
        super().__init__()
        self.fixing_frequency = fixing_frequency
        self.fixing_ric_source = fixing_ric_source
        self.fixing_start_date = fixing_start_date
        self.include_holidays = include_holidays
        self.include_weekends = include_weekends

    @property
    def fixing_frequency(self):
        """
        The fixing's frequency. Possible values:
         - Daily
         - Weekly
         - BiWeekly
         - Monthly
         - Quaterly
         - SemiAnnual
         - Annual
        :return: enum FixingFrequency
        """
        return self._get_enum_parameter(FixingFrequency, "fixingFrequency")

    @fixing_frequency.setter
    def fixing_frequency(self, value):
        self._set_enum_parameter(FixingFrequency, "fixingFrequency", value)

    @property
    def fixing_ric_source(self):
        """
        The fixing's RIC source.
        Default value: the first available source RIC of the Fx Cross Code
        :return: str
        """
        return self._get_parameter("fixingRicSource")

    @fixing_ric_source.setter
    def fixing_ric_source(self, value):
        self._set_parameter("fixingRicSource", value)

    @property
    def fixing_start_date(self):
        """
        The beginning date of the fixing period.
        :return: str
        """
        return self._get_parameter("fixingStartDate")

    @fixing_start_date.setter
    def fixing_start_date(self, value):
        self._set_parameter("fixingStartDate", value)

    @property
    def include_holidays(self):
        """
        Include the holidays in the list of fixings
        :return: bool
        """
        return self._get_parameter("includeHolidays")

    @include_holidays.setter
    def include_holidays(self, value):
        self._set_parameter("includeHolidays", value)

    @property
    def include_weekends(self):
        """
        Include the week-ends in the list of fixings
        :return: bool
        """
        return self._get_parameter("includeWeekEnds")

    @include_weekends.setter
    def include_weekends(self, value):
        self._set_parameter("includeWeekEnds", value)
