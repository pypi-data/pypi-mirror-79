# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import asyncio
import logging
import re
from threading import Lock

from refinitiv.dataplatform.delivery.stream import OMMItemStream, StreamState
from .ChainRecord import ChainRecord10Chars, ChainRecord17Chars, ChainRecord32Chars
from .DisplayTemplate import DisplayTemplate


###############################################################
#
#   REFINITIV IMPORTS
#


###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   CLASS DEFINITIONS
#

class StreamingChain(object):
    """
    StreamingChain is designed to request streaming chains and decode it dynamically.
    This class also act like a cache for each part of the chain record.
    """

    #   streaming information specific to streaming chain records
    #       domain
    _StreamingDomain = 'MarketPrice'
    #       service
    _StreamingService = 'IDN_RDF'
    #       field (empty list means all fields)
    _StreamingFields = []

    #   response message from streaming
    _ResponseMessageFieldsName = 'Fields'

    #   chain record pattern in regular expression format
    _ChainRecordPattern = r'^((?P<sequence>[0-9]+)#)*(?P<RIC>[\w\W]+)$'

    #   default number of initialize concurrent decode streams
    _DefaultNumInitializeConcurrentDecodeStreams = 1

    def __init__(self, name,
                 session=None,
                 service=None,
                 #   option for chain constituents
                 skip_summary_links=True,
                 skip_empty=True,
                 override_summary_links=None,
                 #   callbacks
                 on_add=None,
                 on_remove=None,
                 on_update=None,
                 on_complete=None,
                 on_error=None
                 ):

        ########################################################################
        #   chain record properties

        #   store chain record name
        self._name = name
        self._rootChainRecordName = None

        #   service
        self._service = service

        #   store session use default session if session doesn't provided
        from refinitiv.dataplatform.legacy.tools import DefaultSession
        self._session = session if session else DefaultSession.get_default_session()

        #   display template of this chain record
        self._displayTemplateLock = Lock()
        self._displayTemplate = None

        #   store a list of decoded constituents
        self._constituentListLock = Lock()
        self._constituentList = None

        ########################################################################
        #   callback functions

        #   store the callback functions from stream
        #       on_add event happen when new constituent added the chain record
        self._on_add_callback_func = on_add
        self._on_remove_callback_func = on_remove
        self._on_update_callback_func = on_update
        self._on_complete_callback_func = on_complete
        self._on_error_callback_func = on_error

        ########################################################################
        #   streaming properties

        #   mapping dict of each streaming chains to contruct this given chain
        #       note that completed chain record may construct from multiple chain records
        #       ie. complete chain record named ".DJI" contains with three chain records including
        #           "0#.DJI", "1#.DJI", "2#.DJI"
        self._chainRecordNameToItemStreamDictLock = Lock()
        self._chainRecordNameToItemStreamDict = {}

        #   mapping chain record name to each chain record item stream
        self._chainRecordNameToStatusDictLock = Lock()
        self._chainRecordNameToStatusDict = {}

        #   mapping chain record name to chain record
        self._chainRecordNameToChainRecordDictLock = Lock()
        self._chainRecordNameToChainRecordDict = {}

        #   dictionary mapping between chain record name and future object
        self._chainRecordNameToFutureDictLock = Lock()
        self._chainRecordNameToFutureDict = {}

        #   store is the chain record decode completed or not?
        self._is_complete_decoded = self._session._loop.create_future()  # asyncio.Future()

        #   store the chain record name to the number of offset to this chain record from the root of the chain record
        self._chainRecordNameToNumOffsetsFromRootChainRecordDict = {self._name: 0}

        #   remaining update messages to be processed
        self._remainingUpdateMessageListLock = Lock()
        self._remainingUpdateMessageList = []

        ########################################################################
        #   snapshot properties

        #   store skip summary links and skip empty
        self._skipSummaryLinks = skip_summary_links
        self._skipEmpty = skip_empty

        #   store the override number of summary links
        self._override_summary_links = override_summary_links

        #   this is a mapping between display template ot number of summary link
        #       this is used for skip summary link
        self._displayTemplateToNumSummaryLinks = DisplayTemplate.DefaultDisplayTemplateToNumSummaryLinksDict

        #   call an initialize function for constructing the streaming for this chain record
        self._initializeDecodingChainRecord()

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._name}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self._name}>"

    ###############################################################
    #   properties

    @property
    def _num_summary_links(self):
        """ return number of summary links. this could be override by user
                it possible that number of summary links return None if it is a invalid chain record.
        """

        #   get number of summary links from display template
        if self._override_summary_links:
            #   override number of summary links
            return self._override_summary_links
        else:
            #   use the provided number of summary links from display tempalte
            with self._displayTemplateLock:
                return self._displayTemplateToNumSummaryLinks.get(self._displayTemplate, None)

    @property
    def name(self):
        return self._name

    @property
    def is_chain(self):
        """ return of this property is blocking until self._is_complete_decoded is done

    Returns
    -------
    boolean
        True if it is a chain record, otherwise False
        """
        return self._session._loop.run_until_complete(self._is_chain_async())
        # if self._is_complete_decoded.done():
        #     return self._session._loop.run_until_complete(self._is_chain_async())
        # else:
        #     return None

    @property
    def summary_links(self):
        """ return of this property is blocking until self._is_complete_decoded is done

    Returns
    -------
    list
        a list of the summary links of this chain record, if the chain record is valid
        otherwise, return None
        """

        #   check is this an invalid chain record or not?
        if not self.is_chain:
            #   this is not a chain record, so not constituents, return None
            return None

        #   get number of summary links in this chain record
        numSummaryLinks = self._num_summary_links

        #   get summary links from stream
        summaryLinkList = self._constituentList[:numSummaryLinks]

        #   do skip None and return
        return [summaryLink for summaryLink in summaryLinkList if not self._skipEmpty or summaryLink != None]

    async def _is_chain_async(self):
        """ This function is used for checking is this a chain or not ? """
        #   wait for until complete received all parts to construct this chain record
        await self._is_complete_decoded

        #   at this point chains are complete received

        #   check the given chain record name is invalid or not? 
        with self._chainRecordNameToChainRecordDictLock:
            #   check for chain record name is valid or not?
            return True if self._chainRecordNameToChainRecordDict.get(self._name, None) != None else False

    def get_constituents(self):
        """ return of this property is blocking until self._is_complete_decoded is done
                return None, if its is an invalid chain record
    Returns
    -------
    list
        a list of constituents in the chain record, if it is a valid chain record,
        otherwise, return empty list []
        """

        #   check is this an invalid chain record or not?
        if not self.is_chain:
            #   this is not a chain record, so not constituents, return empty list
            #   (don't return None to avoid exception when iterate on StreamingChain)
            return []

        #   get number of summary links in this chain record
        numSummaryLinks = self._num_summary_links

        #   copy constituents from stream and do skip summary links if skipSummaryLinks is True
        constituentList = self._constituentList[numSummaryLinks:] if self._skipSummaryLinks else self._constituentList[:]

        #   do skip None and return
        return [constituent for constituent in constituentList if not self._skipEmpty or constituent != None]

    def get_display_name(self):
        """
        Returns
        -------
        str
            a value of DSPLY_NAME field if it exist, otherwise empty string
        """
        #   check is this an invalid chain record or not?
        if not self.is_chain:
            # this is not a chain record, so not constituents, return empty string
            return ''

        #   get the first chain display name and return
        with self._chainRecordNameToChainRecordDictLock:
            #   check for chain record name is valid or not?
            chainRecord = self._chainRecordNameToChainRecordDict.get(self._name, None)
            return chainRecord.displayName if chainRecord.displayName != None else ''

    ###############################################################
    #   iterator/getitem functions

    def __iter__(self):
        #   iterate over a snapshot of constituents of this chain record
        yield from self.get_constituents()

    def __getitem__(self, index):
        #   return constituent at given index
        constituentList = self.get_constituents()
        return constituentList[index] if constituentList else None

    def __len__(self):
        return len(self.get_constituents())

    ###############################################################
    #   initialize functions

    def _initializeDecodingChainRecord(self):
        """ initialize the stream for all chain records in the chain record name """

        #   construct the given chain record
        self._constructChainRecordStream(self._name)

        ##################################################
        #   the following steps are an optimization
        #       by construct all possible chain records 
        #       when open() is called it will stream parallel all possible chains

        #   match the chain to get RIC and chain sequence number
        matched = re.match(self._ChainRecordPattern, self._name)
        assert (matched != None)

        #   get the chain record name
        matchedDict = matched.groupdict()
        self._rootChainRecordName = matchedDict['RIC']

        #   ready to start the streaming for chain records 
        #       this are construct all possible chains
        for i in range(1, self._DefaultNumInitializeConcurrentDecodeStreams):
            #   construct the chain record name
            thisChainRecordName = r'{}#{}'.format(i, self._rootChainRecordName)

            #   construct item stream for this chain record
            self._constructChainRecordStream(thisChainRecordName)

    def _constructChainRecordStream(self, chainRecordName):
        """ construct new item streaming for given chain record name
                and store it as a mapping from chain record name
        """
        with self._chainRecordNameToItemStreamDictLock:
            assert (chainRecordName not in self._chainRecordNameToItemStreamDict)

        #   construct and run the item stream
        thisChainRecordItemStream = OMMItemStream(session=self._session,
                                               name=chainRecordName,
                                               domain=self._StreamingDomain,
                                               service=self._service,
                                               fields=self._StreamingFields,
                                               on_refresh=self._on_refresh,
                                               on_status=self._on_status,
                                               on_update=self._on_update,
                                               on_complete=self._on_complete,
                                               on_error=self._on_error)

        #   store the mapping between chain record name to stream
        with self._chainRecordNameToItemStreamDictLock:
            self._chainRecordNameToItemStreamDict[chainRecordName] = thisChainRecordItemStream

        with self._chainRecordNameToFutureDictLock:
            self._chainRecordNameToFutureDict[chainRecordName] = self._session._loop.create_future() # asyncio.Future()

        #   done, return this chain record item stream
        return thisChainRecordItemStream

    def _hasChainRecordStream(self, chainRecordName):
        """ check given chain record has item stream or not ? """
        with self._chainRecordNameToItemStreamDictLock:
            return True if chainRecordName in self._chainRecordNameToItemStreamDict else False

    def _hasChainRecord(self, chainRecordName):
        """ check given chain record has chain record object or not ? """
        with self._chainRecordNameToChainRecordDictLock:
            return True if chainRecordName in self._chainRecordNameToChainRecordDict else False

    ############################################################
    #   open/close streaming chain functions

    def open(self, with_updates=True):
        """ open chain record item streams """
        return self._session._loop.run_until_complete(self._decode_async(with_updates=with_updates))

    async def open_async(self, with_updates=True):
        """ open chain record with asynchronous decoding """
        return await self._decode_async(with_updates=with_updates)

    async def _decode_async(self, with_updates=True):
        """ open all chain record stream and decode it"""
        self._session.log(logging.INFO, 'StreamingChain :: Processing decode chain record {}.'.format(self._name))

        #   loop over all initial set of stream for this chains and open it
        with self._chainRecordNameToItemStreamDictLock:
            for chainRecordName, itemStream in list(self._chainRecordNameToItemStreamDict.items()):
                #   open each chain record stream
                self._session.log(logging.INFO, 'Opening stream of chain record = {}.'.format(chainRecordName))
                await itemStream.open_async(with_updates=with_updates)

        # check if all chain records were received without error

        ############################################################
        #   now let's start decode given chain record

        #   initialize the list of constituents to be assmble
        with self._constituentListLock:
            self._constituentList = []

        #   initialize the dictionary mapping between chain record name to offset from root of chain recrd
        numOffsetFromRootChainRecord = 0

        #   loop until next chain record is None
        thisChainRecordName = self._name
        while thisChainRecordName:

            # #   store the order for decoding this chain record
            # self._orderedDecodeChainRecordNameList.append(thisChainRecordName)

            #   check this chain are opened for stream or not?
            if not self._hasChainRecordStream(thisChainRecordName):
                #   this chain record doesn't open as streaming yet, so construct the stream and open it
                #   construct chain record stream
                thisChainRecordStream = self._constructChainRecordStream(thisChainRecordName)

                #   open stream
                await thisChainRecordStream.open_async(with_updates=with_updates)

            #   wait for this stream response ONLY IF STATUS IS NOT CLOSED
            _status = self._chainRecordNameToStatusDict[chainRecordName].get("status")
            if _status == StreamState.Closed:
                #   finished decode chain, so set the complete decoded flags to be False
                self._is_complete_decoded.set_result(False)
            else:
                await self._chainRecordNameToFutureDict[thisChainRecordName]

            #   check this chain record is already open as stream and its chain recrd is ready or not?
            with self._chainRecordNameToChainRecordDictLock:
                #   get this chain record object
                thisChainRecord = self._chainRecordNameToChainRecordDict.get(thisChainRecordName, None)

            #   check this chain record is valid or not?
            if thisChainRecord:
                #   this is a valid chain record, so get the next chain response chain record

                #   get next chain record for this chain
                nextChainRecordName = thisChainRecord.nextChainRecordName

                #   assemble the constituents of the chain record
                for index, constituent in enumerate(thisChainRecord.constituentList):
                    self._append_constituent(numOffsetFromRootChainRecord + index, constituent)

                #   store the offset to this chain record
                self._chainRecordNameToNumOffsetsFromRootChainRecordDict[thisChainRecordName] = numOffsetFromRootChainRecord
                numOffsetFromRootChainRecord += thisChainRecord.numConsituents if thisChainRecord.numConsituents else 0

            else:
                #   something wrong, we should wait for frist response from interested chain record stream
                #       and each stream chain should be construct and got response
                #   it's an invalid chain record, so done
                self._session.log(logging.ERROR,
                                  "StreamingChain :: Stopped to process chain record because it found an invalid chain record {}.".format(
                                      chainRecordName))
                # Send error
                if self._on_error_callback_func:
                    self._on_error_callback_func(self, chainRecordName, itemStream.status)
                break

            #   done set next chain record to be decoded
            thisChainRecordName = nextChainRecordName
            self._session.log(20, 'StreamingChain :: Processing decode next chain record {}.'.format(nextChainRecordName))

        #   finished decode chain, so set the complete decoded flags to be True
        if not self._is_complete_decoded.done():
            self._is_complete_decoded.set_result(True)

        #   call the complete decoded callback
        if self._on_complete_callback_func:
            #   do call the complete decoded callback function
            self._on_complete_callback_func(self, self.get_constituents())

        #   process remaining update message due to waiting to decode finished
        self._processRemainingUpdateMessages()

        self._session.log(logging.INFO, 'StreamingChain :: DONE - Processing decode chain record {}.'.format(self._name))

        #  return the list of constituents in this chain
        return self.get_constituents()

    def close(self):
        """ close chain record item streams """
        #   loop over all initial set of stream for this chains and close it
        with self._chainRecordNameToItemStreamDictLock:
            for chainRecordName, itemStream in list(self._chainRecordNameToItemStreamDict.items()):
                #   close each chain record stream
                self._session.log(logging.INFO, 'Closing stream of chain record = {}.'.format(chainRecordName))
                itemStream.close()

    ###############################################################
    #   internal processing response chain record functions

    def _processChainRecord(self, chainRecordName, message):
        """
        This function is designed for processing chain record. this will happen when got the refresh response.
        The processing steps are parsing the response message, request next chain record from stream if it doesn't exist
        """
        self._session.log(logging.INFO, 'StreamingChain :: Processing response chain record {}, message = {}.'.format(chainRecordName, message))

        #   get the fields from response message
        fields = message[self._ResponseMessageFieldsName] if self._ResponseMessageFieldsName in message else []

        #   do parse the response message to construct the chain object
        self._parseChainRecord(chainRecordName, fields)

    def _parseChainRecord(self, chainRecordName, fields):
        """
        Parse the chain record then construct chain record and store as a mapping between chain record name
         to chain record object.
        """
        self._session.debug('StreamingChain :: Parsing response field of chain record {}, field = {}.'.format(chainRecordName, fields))

        #   check the check the chain record template
        #       there are three chain record templates (template #80, template #85 and template #32766)
        if ChainRecord17Chars.isValidChainRecord(fields):
            #   this is a chain record for 17 chars, so extract it
            chainRecord = ChainRecord17Chars.parseChainRecord(fields)
        elif ChainRecord10Chars.isValidChainRecord(fields):
            #   this is a chain record for 10 chars, so extract it
            chainRecord = ChainRecord10Chars.parseChainRecord(fields)
        elif ChainRecord32Chars.isValidChainRecord(fields):
            #   this is a chain record for 32 chars, so extract it
            chainRecord = ChainRecord32Chars.parseChainRecord(fields)
        else:
            #   invalid chain record template
            #       so close this stream and set the result as not a chain record
            self._session.log(logging.ERROR, 'StreamingChain :: Cannot parse chain {} because it is an invalid chain.'.format(chainRecordName))
            #   do nothing, done
            return

        #   store in the mapping between streaming name to chain record
        with self._chainRecordNameToChainRecordDictLock:
            assert (chainRecordName not in self._chainRecordNameToChainRecordDict)
            self._chainRecordNameToChainRecordDict[chainRecordName] = chainRecord

        #   store the display template
        with self._displayTemplateLock:
            if not self._displayTemplate:
                #   this is a first time that parsing forund display template properties on this chain record, so store it
                self._displayTemplate = chainRecord.displayTemplate
            else:
                #   the display template on the chain recrod must be the same
                assert (self._displayTemplate == chainRecord.displayTemplate)

        self._session.debug('StreamingChain :: DONE - Parsing response field of chain record {}, field = {}.'.format(chainRecordName, fields))

        #   done, return chain record
        return chainRecord

    def _updateChainRecord(self, chainRecordName, update):
        """ update existing chain record """
        self._session.log(logging.INFO, 'StreamingChain :: Updating response field of chain record {}, update = {}.'.format(chainRecordName, update))

        #   get the fields fromt response message
        fields = update[self._ResponseMessageFieldsName] if self._ResponseMessageFieldsName in update else []

        #   get the parsed chain record, according to the update
        with self._chainRecordNameToChainRecordDictLock:
            #   extract the chain record from mapping dict and modify
            chainRecord = self._chainRecordNameToChainRecordDict.get(chainRecordName, None)

        #   check this chain record are valid or not?
        if not chainRecord:
            #   invalid chain record, so don't need to call an update
            #       skip it
            self._session.log(logging.WARNING, 'StreamingChain :: Skipping to update an invalid chain record = {}.'.format(chainRecordName))
            return

        #   update the chain record
        chainRecordUpdateInfo = chainRecord.update(fields)

        assert (chainRecordUpdateInfo != None)
        #   do update the constituents
        assert (self._chainRecordNameToNumOffsetsFromRootChainRecordDict != None)
        assert (chainRecordName in self._chainRecordNameToNumOffsetsFromRootChainRecordDict)
        offsetFromRootChainRecord = self._chainRecordNameToNumOffsetsFromRootChainRecordDict[chainRecordName]
        for index, (oldConstituent, newConstituent) in list(chainRecordUpdateInfo.indexToOldAndNewConstituentTupleDict.items()):
            #   determine relative index from root of the chain to this chain record
            relativeIndex = offsetFromRootChainRecord + index

            #       check if old/new constituent are not a empty, this mean it updated on this index
            if oldConstituent and newConstituent:
                #   this is an update constituent, so call update
                self._update_constituent(relativeIndex, oldConstituent, newConstituent)

            #       check if old constituent is a empty and new constituent is not a sempty, this mean it add on this index
            elif not oldConstituent and newConstituent:
                #   this is an add constituent, so call add
                self._append_constituent(relativeIndex, newConstituent)

            #       check if old constituent is not  aempty and new constituent is a empty, this mean it remove on this index
            elif oldConstituent and not newConstituent:
                #   this is an add constituent, so call remove
                self._remove_constituent(relativeIndex, oldConstituent)

        self._session.log(logging.INFO, 'StreamingChain :: chain record update info = {}.'.format(chainRecordUpdateInfo))

    # warning CODE_ME if prev/next field are changed. It rarely those fields are chainged.

    def _processRemainingUpdateMessages(self):
        """ this function is designed for processing the remaining update message due to wait for decode completed """
        self._session.log(logging.INFO, 'StreamingChain :: Processing remaining update messages.')

        #   loop until all remaining update messages processed
        while True:

            #   try pop the update message from the list
            try:
                with self._remainingUpdateMessageListLock:
                    (streamName, updateMessage) = self._remainingUpdateMessageList.pop(0)
            except IndexError:
                #   no remaining update message, done
                break

            #   prcoess remaining update message
            self._updateChainRecord(streamName, updateMessage)

        #   done
        self._session.log(logging.INFO, 'StreamingChain :: DONE - Processing remaining update messages.')

    ###############################################################
    #   internal add/remove/update constituents in the chain record functions

    def _add_constituent(self, index, constituent):
        """ add new constituent to the chain record """
        self._session.log(10, 'StreamingChain.add_constituent(index = {}, constituent = {})'.format(index, constituent))
        assert (index >= 0 and index <= len(self._constituentList))

        #   replace constituent from None
        with self._constituentListLock:
            assert (self._constituentList[index])
            self._constituentList[index] = constituent

        #   do call the callback function when add new constituent
        if self._on_add_callback_func:
            #   call the add callback function
            self._on_add_callback_func(self, index, constituent)

    def _append_constituent(self, index, constituent):
        """ append new constituent to the chain record
                note that this function use when decode the chain record
        """
        self._session.log(10, 'StreamingChain.append_constituent(index = {}, constituent = {})'.format(index, constituent))
        assert (index == len(self._constituentList))

        #   append new constituent to the chain record
        with self._constituentListLock:
            self._constituentList.append(constituent)

        #   do call the callback function when add new constituent
        if self._on_add_callback_func:
            #   call the add callback function
            self._on_add_callback_func(self, index, constituent)

    def _remove_constituent(self, index, constituent):
        """ remove the index in constituent to be None """
        self._session.log(10, 'StreamingChain.remove_constituent(index = {}, constituent = {})'.format(index, constituent))
        assert (index >= 0 and index < len(self._constituentList))

        #   do remove given index in the chain record
        with self._constituentListLock:
            assert (self._constituentList[index])
            self._constituentList.pop(index)

        #   do call the callback function when constituent removed
        if self._on_remove_callback_func:
            #   call remove callback function
            self._on_remove_callback_func(self, index, constituent)

    def _update_constituent(self, index, oldConstituent, newConstituent):
        """ update the constituent in the chain record """
        self._session.log(10, 'StreamingChain.update_constituent(index = {}, oldConstituent = {}, newConstituent = {})'.format(index, oldConstituent,
                                                                                                                               newConstituent))
        assert (index >= 0 and index < len(self._constituentList))

        #   do update given constituent in the chain record
        with self._constituentListLock:
            self._constituentList[index] = newConstituent

        #   do call the callback when constituent in the chain record is updated
        if self._on_update_callback_func:
            #   call the update callback
            self._on_update_callback_func(self, index, oldConstituent, newConstituent)

    ###############################################################
    #   internal handle stream callback functions

    def _on_refresh(self, stream, message):
        """ streaming callback function on refresh """
        self._session.log(20, 'StreamingChain.on_refresh(stream = {}, message = {})'.format(stream.name, message))

        #   get chain record name
        chainRecordName = stream.name

        #   do process the refresh
        self._processChainRecord(stream.name, message)

        #   change future flag on this chain record stream
        with self._chainRecordNameToFutureDictLock:
            streamResponseFuture = self._chainRecordNameToFutureDict[chainRecordName]
#warning :: PREVENT AND ERROR WHEN IT HAS MULTIPLE REFRESH MESSAGE FROM SERVER
#               PLEASE RECHECK THE PROTOCOL ON SERVER SIDE
            if not streamResponseFuture.done():
            #   it's possible that it's receiving a refresh message multiple time from server
                self._session._loop.call_soon_threadsafe(streamResponseFuture.set_result, True)

    def _on_update(self, stream, update):
        """ streaming callback function on update """
        self._session.log(20, 'StreamingChain.on_update(stream = {}, update = {})'.format(stream.name, update))

        #   check updating chain is ready to update
        #       Did it finish decode the chain record?
        if not self._is_complete_decoded.done():
            #   it's still decoding the chain record,
            #       the update will be occur after the chain decode completed
            #   store the postpone update message
            with self._remainingUpdateMessageListLock:
                self._remainingUpdateMessageList.append((stream.name, update))

            #   do nothing
            self._session.log(logging.WARNING, 'StreamingChain :: waiting to update because chain decode does not completed.')
            return

        #   process remaining update message due to waiting to decode finished
        self._processRemainingUpdateMessages()

        #   do process the update
        self._updateChainRecord(stream.name, update)

    def _on_status(self, stream, status):
        """ streaming callback function on status """
        self._session.log(20, 'StreamingChain.on_status(stream = {}, status = {})'.format(stream.name, status))

        #   get chain record name
        chainRecordName = stream.name

        #   store the status of chain record streaming
        with self._chainRecordNameToStatusDictLock:
            self._chainRecordNameToStatusDict[chainRecordName] = status

        state = status.get("Status")
        if state == "Closed":
            if not streamResponseFuture.done():
                #   it's possible that it's receiving a refresh message multiple time from server
                self._session._loop.call_soon_threadsafe(streamResponseFuture.set_result, True)

    def _on_complete(self, stream):
        """ streaming callback function on complete """
        self._session.log(20, 'StreamingChain.on_complete(stream = {})'.format(stream.name))

        #   do nothing
        pass

    def _on_error(self, stream, error):
        """ streaming callback function on error """
        self._session.log(20, 'StreamingChain.on_error(stream = {}, error = {})'.format(stream.name, error))

        #   call the registered callback function
        if self._on_error_callback_func:
            #   callback function was registered, so call the callback function
            self._on_error_callback_func(self, stream.name, error)
