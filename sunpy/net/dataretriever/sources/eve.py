# Author: Rishabh Sharma <rishabh.sharma.gunner@gmail.com>
# This module was developed under funding by
# Google Summer of Code 2014

import urlparse

from ..client import GenericClient


__all__ = ['EVEClient']


class EVEClient(GenericClient):
    """
    This EVEClient is for the Level 0C data
    from http://lasp.colorado.edu/home/eve/data/data-access/.

    To use this client you must request Level 0 data.

    Examples
    --------

    >>> results = Fido.search(a.Time("2016/1/1", "2016/1/2"),
                              a.Instrument('EVE'), a.Level(0))
    >>> results
    [<Table length=2>
        Start Time           End Time      Source Instrument
          str19               str19         str3     str3
    ------------------- ------------------- ------ ----------
    2016-01-01 00:00:00 2016-01-02 00:00:00    SDO        eve
    2016-01-02 00:00:00 2016-01-03 00:00:00    SDO        eve]
    """

    def _get_url_for_timerange(self, timerange, **kwargs):
        """
        Returns list of URLS corresponding to value of input timerange.

        Parameters
        ----------
        timerange: sunpy.time.TimeRange
            time range for which data is to be downloaded.

        Returns
        -------
        urls : list
            list of URLs corresponding to the requested time range
        """
        days = timerange.get_dates()
        urls = []
        for day in days:
            urls.append(self._get_url_for_date(day, **kwargs))
        return urls

    def _get_url_for_date(self, date, **kwargs):
        """
        Return URL for corresponding date.

        Parameters
        ----------
        date : Python datetime object

        Returns
        -------
        URL : string
        """
        base_url = 'http://lasp.colorado.edu/eve/data_access/evewebdata/quicklook/L0CS/SpWx/'
        return urlparse.urljoin(base_url,
                                date.strftime('%Y/%Y%m%d') + '_EVE_L0CS_DIODES_1m.txt')

    def _makeimap(self):
        """
        Helper Function: used to hold information about source.
        """
        self.map_['source'] = 'SDO'
        self.map_['provider'] = 'LASP'
        self.map_['instrument'] = 'eve'
        self.map_['phyobs'] = 'irradiance'

    @classmethod
    def _can_handle_query(cls, *query):
        """
        Answers whether client can service the query.

        Parameters
        ----------
        query : list of query objects

        Returns
        -------
        boolean
            answer as to whether client can service the query
        """
        chk_var = 0
        for x in query:
            if x.__class__.__name__ == 'Instrument' and x.value.lower() == 'eve':
                chk_var += 1

            elif x.__class__.__name__ == 'Level' and x.value == 0:
                chk_var += 1

        if chk_var == 2:
            return True
        return False
