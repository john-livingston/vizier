import os
import sys
import numpy as np
import pandas as pd
import urllib, urllib2
from astropy.io.votable import parse_single_table


class Vizier(object):

    def __init__(self):
        self._handler = None
        self._handler_is_done = False

    def _get_url(self):
        raise NotImplementedError

    def query(self, *args):

        url = self._get_url(*args)
        print "Retrieving: {}".format(url)
        self._handler = urllib2.urlopen(url)

        return self.df

    @property
    def df(self):

        assert self._handler is not None

        if not self._handler_is_done:
            table = parse_single_table(self._handler)
            self._df = pd.DataFrame.from_records(table.array)

        self._handler_is_done = True

        return self._df


class PPMXL(Vizier):

    def _get_url(self, ra, dec, radius):

            """
            Returns the URL for a HTTP query of the PPMXL catalog via ViZieR.
            Query is centered on <ra>, <dec> (decimal degrees or sexigesimal),
            with radius <radius> in degrees. URL will request data in XML/VOTable
            format.
            """

            url = 'http://vizier.u-strasbg.fr/viz-bin/votable'
            p = {}
            p['-source'] = 'I/317'
            if type(dec) is float:
                if np.sign(dec) > 0:
                    p['-c'] = '{0:0.4f}+{1:0.4f}'.format(ra, dec)
                else:
                    p['-c'] = '{0:0.4f}{1:0.4f}'.format(ra, dec)
            else:
                p['-c'] = '{0}{1}'.format(ra, dec)
            p['-c.rd'] = '{}'.format(radius)
            p['-out.max'] = 999999999
            query = urllib.urlencode(p)
            query_url = url + "?" + query

            return query_url
