# coding: utf8

__all__ = ["StreamingPrices"]

import asyncio
import sys

from pandas import DataFrame

from refinitiv.dataplatform.content.streaming.streamingprice import StreamingPrice
from refinitiv.dataplatform.delivery.stream import StreamState, Openable
from refinitiv.dataplatform.errors import StreamingPricesError


class StreamingPrices(Openable):
    """
    Open a streaming price subscription.

    Parameters
    ----------
    universe: list[string]
        List of RICs to subscribe.

    service: string
        Specified the service to subscribe on.
        Default: None

    fields: string or list[string]
        Specified the fields to retrieve.
        Default: None

    on_refresh: callable object (streaming_prices, instrument_name, message)
        Called when a stream on instrument_name was opened successfully or when the stream is refreshed by the server.
        This callback is called with the reference to the streaming_prices object, the instrument name and the instrument full image.
        Default: None

    on_update: callable object (streaming_prices, instrument_name, message)
        Called when an update is received for a instrument_name.
        This callback is called with the reference to the streaming_prices object, the instrument name and the instrument update.
        Default: None

    on_status: callable object (streaming_prices, instrument_name, status)
        Called when a status is received for a instrument_name.
        This callback is called with the reference to the streaming_prices object, the instrument name and the instrument status.
        Default: None

    on_complete: callable object  (streaming_prices, instrument_name)
        Called when all subscriptions are completed.
        This callback is called with the reference to the streaming_prices object.
        Default: None

    Raises
    ------
    Exception
        If request fails.

    Examples
    --------
    >> import eikon as ek
    >> fx = ek.StreamingPrices(['EUR=', 'GBP='])
    >> fx.open()
    >> bid_eur = fx['EUR']['BID']
    >> ask_eur = fx['EUR']['ASK']
    >>
    >> def on_update(streams, instrument, msg):
            ... print(msg)
    >> subscription = ek.StreamingPrices(['VOD.L', 'EUR=', 'PEUP.PA', 'IBM.N'],
            ... ['DSPLY_NAME', 'BID', 'ASK'],
            ... on_update=on_update)
    >> subscription.open()
    {"EUR=":{"DSPLY_NAME":"RBS          LON","BID":1.1221,"ASK":1.1224}}
    {"PEUP.PA":{"DSPLY_NAME":"PEUGEOT","BID":15.145,"ASK":15.155}}
    {"IBM.N":{"DSPLY_NAME":"INTL BUS MACHINE","BID":"","ASK":""}}
    ...
    """

    class Params(object):
        def __init__(self, universe, fields):
            self._universe = universe
            self._fields = fields

        @property
        def universe(self):
            return self._universe

        @property
        def fields(self):
            return self._fields

    class StreamingPricesIterator:
        """ StreamingPrices Iterator class """

        def __init__(self, streaming_prices):
            self._streaming_prices = streaming_prices
            self._index = 0

        def __next__(self):
            """" Return the next streaming item from streaming price list """
            if self._index < len(self._streaming_prices.params.universe):
                result = self._streaming_prices[self._streaming_prices.params.universe[self._index]]
                self._index += 1
                return result
            raise StopIteration()

    def __init__(
            self,
            universe,
            session=None,
            fields=[],
            service=None,
            connection=None,
            on_refresh=None,
            on_status=None,
            on_update=None,
            on_complete=None
    ):

        from refinitiv.dataplatform.legacy.tools import DefaultSession

        if session is None:
            session = DefaultSession.get_default_session()

        super().__init__(loop=session._loop)

        self._session = session

        if isinstance(universe, str):
            universe = [universe]
        elif isinstance(universe, list) and all(isinstance(item, str) for item in universe):
            pass
        else:
            raise StreamingPricesError(-1, "StreamingPrices: universe must be a list of strings")

        self._fields = fields

        self.params = StreamingPrices.Params(universe=universe, fields=fields)

        self._service = service
        self._streaming_prices = {}
        for name in universe:
            self._streaming_prices[name] = StreamingPrice(
                session=self._session,
                name=name,
                fields=self._fields,
                service=self._service,
                connection=connection,
                on_refresh=self._on_refresh,
                on_update=self._on_update,
                on_status=self._on_status,
                on_complete=self._on_complete
            )
        self._on_refresh_cb = on_refresh
        self._on_status_cb = on_status
        self._on_update_cb = on_update
        self._on_complete_cb = on_complete

        self._state = StreamState.Closed
        self._complete_event_nb = 0

        #   set universe of on_complete 
        self._on_complete_set = None

    ###################################################
    #  Access to StreamingPrices as a dict            #
    ###################################################

    def keys(self):
        if self._streaming_prices:
            return self._streaming_prices.keys()
        return {}.keys()

    def values(self):
        if self._streaming_prices:
            return self._streaming_prices.values()
        return {}.values()

    def items(self):
        if self._streaming_prices:
            return self._streaming_prices.items()
        return {}.items()

    ###################################################
    #  Make StreamingPrices iterable                  #
    ###################################################

    def __iter__(self):
        return StreamingPrices.StreamingPricesIterator(self)

    def __getitem__(self, item):
        if item in self.params.universe:
            return self._streaming_prices[item]
        else:
            raise KeyError(f"{item} not in StreamingPrices universe")

    def __len__(self):
        return len(self.params.universe)

    ###################################################
    #  methods to open synchronously item stream      #
    ###################################################

    def _do_pause(self):
        results = [v.pause() for v in self._streaming_prices.values()]
        assert all([r is StreamState.Pause for r in results])

    def _do_resume(self):
        results = [v.resume() for v in self._streaming_prices.values()]
        assert all([r is not StreamState.Pause for r in results])

    ################################################
    #  methods to open asynchronously item stream  #
    ################################################
    async def _do_open_async(self, with_updates=True):
        """
        Open asynchronously the streaming price
        """
        self._session.log(1, f'StreamingPrices : open streaming on {self.params.universe}')
        
        #   reset the on_complete set
        self._on_complete_set = set()
            
        streaming_prices = iter(self._streaming_prices.values())
        stream_opens_socket = next(streaming_prices)
        await stream_opens_socket.open_async(with_updates=with_updates)
        await asyncio.gather(*[i.open_async(with_updates=with_updates) for i in streaming_prices])
        self._session.debug(f'StreamingPrices : start asynchronously streaming on {self.params.universe} done')
        return True

    async def _do_close_async(self):
        self._session.debug(1, f'StreamingPrices : close streaming on {self.params.universe}')
        for stream in self._streaming_prices.values():
            stream.close()

    def get_snapshot(self, universe=None, fields=None, convert=True):
        """
        Returns a Dataframe filled with snapshot values for a list of instrument names and a list of fields.

        Parameters
        ----------
        universe: list of strings
            List of instruments to request snapshot data on.

        fields: list of strings
            List of fields to request.

        convert: boolean
            If True, force numeric conversion for all values.

        Returns
        -------
            pandas.DataFrame

            pandas.DataFrame content:
                - columns : instrument and fieled names
                - rows : instrument name and field values

        Raises
        ------
            Exception
                If request fails or if server returns an error

            ValueError
                If a parameter type or value is wrong

        Examples
        --------
        >>> import eikon as ek
        >>> ek.set_app_key('set your app key here')
        >>> streaming_prices = ek.StreamingPrices(instruments=["MSFT.O", "GOOG.O", "IBM.N"], fields=["BID", "ASK", "OPEN_PRC"])
        >>> data = streaming_prices.get_snapshot(["MSFT.O", "GOOG.O"], ["BID", "ASK"])
        >>> data
              Instrument    BID        ASK
        0     MSFT.O        150.9000   150.9500
        1     GOOG.O        1323.9000  1327.7900
        """

        if universe:
            for name in universe:
                if name not in self.params.universe:
                    raise StreamingPricesError(-1, f'Instrument {name} was not requested : {self.params.universe}')

        if fields:
            for field in fields:
                if field not in self.params.fields:
                    raise StreamingPricesError(-1, f'Field {field} was not requested : {self.params.fields}')

        _universe = universe if universe else self.params.universe
        _all_fields_value = {
            name: self._streaming_prices[name].get_fields(fields)
            if name in self._streaming_prices else None
            for name in _universe
        }
        _fields = []

        if not fields:
            for field_values in _all_fields_value.values():
                if field_values:
                    _fields.extend(field for field in field_values.keys() if field not in _fields)
        else:
            _fields = fields

        _df_source = {
            f: [
                _all_fields_value[name][f]
                if _all_fields_value[name].get(f) else None
                for name in _universe
            ] for f in _fields
        }
        _price_dataframe = DataFrame(_df_source, columns=_fields)
        if convert:
            # _price_dataframe = _price_dataframe.apply(to_numeric, errors='ignore')
            if not _price_dataframe.empty:
                _price_dataframe = _price_dataframe.convert_dtypes()
        _price_dataframe.insert(0, 'Instrument', _universe)

        return _price_dataframe

    #########################################
    # Messages from stream_cache connection #
    #########################################
    def _on_refresh(self, stream, message):

        if self.is_pause():
            return

        if self._on_refresh_cb:
            try:
                self._session.log(1, 'StreamingPrices : call on_refresh callback')
                self._session._loop.call_soon_threadsafe(self._on_refresh_cb, self, stream.name, message)
            except Exception as e:
                self._session.error(f'StreamingPrices on_refresh callback raised exception: {e!r}')
                self._session.log(1, f'Traceback : {sys.exc_info()[2]}')

    def _on_status(self, stream, status):

        if self.is_pause():
            return

        if self._on_status_cb:
            try:
                # if self._state == StreamState.Pending:
                #     should set state to Open ?

                self._session.log(1, 'StreamingPrices : call on_status callback')
                self._session._loop.call_soon_threadsafe(self._on_status_cb, self, stream.name, status)
            except Exception as e:
                self._session.error(f'StreamingPrices on_status callback raised exception: {e!r}')
                self._session.log(1, f'Traceback : {sys.exc_info()[2]}')
        
        #   check for closed stream when status "Closed", "ClosedRecover", "NonStreaming" or "Redirect"
        if stream.state == StreamState.Closed \
            and stream.name not in self._on_complete_set:
        #   this stream has been closed, so it means completed also
            self._on_complete(stream)

    def _on_update(self, stream, update):

        if self.is_pause():
            return

        if self._on_update_cb:
            try:
                self._session.log(1, 'StreamingPrices : call on_update callback')
                self._session._loop.call_soon_threadsafe(self._on_update_cb, self, stream.name, update)
            except Exception as e:
                self._session.error(f'StreamingPrices on_update callback raised exception: {e!r}')
                self._session.log(1, f'Traceback : {sys.exc_info()[2]}')

    def _on_complete(self, stream):
        assert self._on_complete_set is not None

        #   check for update completed set
        if stream.name not in self._on_complete_set:
        #   update the stream to be in complete list
            self._on_complete_set.update([stream.name,])

        if self._on_complete_set == set(self.params.universe):
            # self._state = StreamState.Open

            if self.is_pause():
                return

            if self._on_complete_cb:
                try:
                    self._session.log(1, 'StreamingPrices : call on_complete callback')
                    self._session._loop.call_soon_threadsafe(self._on_complete_cb, self)
                except Exception as e:
                    self._session.error(f'StreamingPrices on_complete callback raised exception: {e!r}')
                    self._session.log(1, f'Traceback : {sys.exc_info()[2]}')
            