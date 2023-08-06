# coding: utf-8

###############################################################
#
#   STANDARD IMPORTS
#

import abc

import urllib.parse

import logging

import requests_async as requests

###############################################################
#
#   REFINITIV IMPORTS
#

from refinitiv.dataplatform.errors import EnvError

###############################################################
#
#   LOCAL IMPORTS
#

from .service_discovery_information import ServiceDiscoveryBeta1Information, \
                                            ServiceDiscoveryV1Information

###############################################################
#
#   CLASSE DEFINITIONS
#


class StreamingConnectionConfiguration(abc.ABC):
    """ this class is designed for store the streaming connection configuration """

    class StreamReconnectionConfiguration(object):
        """ This class is designed to handle the websocket reconnection configuration """

        #   default delay time before do a reconnection in secs
        _DefaultReconnectionDelayTime_secs = 5

        #   default reset the reconnection time after last requested uri
        _DefaultResetReconnectionTime_secs = 120.0

        def __init__(self, websocket_endpoints=None, secure=None):
            #   store all of possible websocket endpoints
            self._websocket_endpoints = [] if websocket_endpoints is None else websocket_endpoints
            self._secure = True if secure is None else secure

            #   store the current reconnection configuration
            self._num_reconnection = 0
            self._reconnection_delay_secs = 0

            #   current websocket endpoint index
            self._current_websocket_endpoint_index = 0
            self._start_websocket_endpoint_index = 0

        @property
        def secure(self):
            return self._secure

        @secure.setter
        def secure(self, secure):
            self._secure = secure
            #   reset config
            self.reset()

        @property
        def websocket_endpoints(self):
            return self._websocket_endpoints

        @websocket_endpoints.setter
        def websocket_endpoints(self, websocket_endpoints):
            self._websocket_endpoints = websocket_endpoints
            #   reset config
            self.reset()

        @property
        def uris(self):
            return [self._build_websocket_uri(websocket_endpoint, self.secure)
                    for websocket_endpoint in self._websocket_endpoints]

        @property
        def reconnection_delay_secs(self):
            return self._reconnection_delay_secs

        def initialize_websocket_uri(self, websocket_endpoints, secure):
            assert len(websocket_endpoints) > 0
            self._websocket_endpoints = websocket_endpoints
            self._secure = secure
            return self._build_websocket_uri(self._websocket_endpoints[0], self._secure)

        def next_websocket_uri(self):
            """ This function is used to get next available websocket uri.
                    This function also calculate the waiting time and count the number of reconnection if it still doesn't successful
            """

            #   get number of websocket endpoints
            num_websocket_endpoints = len(self._websocket_endpoints)

            #   construct uri from websocket list
            self._current_websocket_endpoint_index = (self._current_websocket_endpoint_index + 1) % num_websocket_endpoints
            websocket_uri = self._build_websocket_uri(self._websocket_endpoints[self._current_websocket_endpoint_index],
                                                      self._secure)

            #   check for increase the reconnection delay
            if self._num_reconnection != 0 and self._num_reconnection % num_websocket_endpoints == 0:
                #   this websocket endpoint is circle around, so do a delay
                #       increase the waiting time if all websockets cannot connect
                delay_multiplier = (self._num_reconnection + 1) // num_websocket_endpoints
                self._reconnection_delay_secs = self._DefaultReconnectionDelayTime_secs * delay_multiplier
            else:
                #   it still has a websocket endpoint to try, so delay will be 0
                self._reconnection_delay_secs = 0

            #   increase counter
            self._num_reconnection += 1

            #   done
            return websocket_uri

        def reset(self):
            """ Reset the calculator for building next websocket uri """
            #   reset
            #       number of reconnection
            self._num_reconnection = 0
            #       delay
            self._reconnection_delay_secs = 0

        @staticmethod
        def _build_websocket_uri(websocket_endpoint, secure):
            return '{}://{}/WebSocket'.format('wss' if secure else 'ws', websocket_endpoint)

    def __init__(self, session, name:str, 
                    platform_url:str, streaming_connection_config:dict):
        #   session
        self._session = session

        #   streaming connection name
        self._name = name

        #   platform url
        self._platform_url = platform_url

        ################################################################
        #   weboscket streaming connection parameters

        #   websocket endpoint uri
        self._uri  = None

        #   websocket endpoint urls
        self._websocket_endpoint_urls = []

        #   connection type secure or not?
        #       True or False
        self._secure = True

        #   dacs application id
        self._application_id = None
        #   dacs position
        self._position = None

        #   protocol
        self._protocol = None

        #   additional header list
        self._additional_header_list = []

        #   call the initialize configuration based on type
        self._initialize_configuration(streaming_connection_config)

        ################################################################
        #   weboscket reconnection parameters

        #   build the stream reconnection configuration
        self._stream_reconnection_config = self.StreamReconnectionConfiguration()
    
    @property
    def uri(self):
        return self._uri

    @property
    def secure(self):
        return self._secure

    @secure.setter
    def secure(self, secure):
        #   check is the secure is changed or not?
        if self._secure is not secure:
            #   secure is changed, so reinitialize it
            self._secure = secure

            #   set secure to reconnection config
            self._stream_reconnection_config.secure = self._secure

            #   re-initialize websocket reconnection uri
            self._initialize_websocket_reconnection()

    @property
    def protocol(self):
        return self._protocol

    @property
    def websocket_endpoints(self):
        return self._websocket_endpoint_urls

    @websocket_endpoints.setter
    def websocket_endpoints(self, websocket_endpoint_urls):
        self._websocket_endpoint_urls = websocket_endpoint_urls

        #   set websocket endpoint to the reconnection config
        self._stream_reconnection_config.websocket_endpoints = self._websocket_endpoint_urls

        #   re-initialize websocket reconnection uri
        self._initialize_websocket_reconnection()

    @property
    def header(self):
        return self._additional_header_list

    @property
    def reconnection_delay_secs(self):
        return self._stream_reconnection_config.reconnection_delay_secs
    
    @abc.abstractmethod
    def _initialize_configuration(self, streaming_connection_config:dict):
        """ initialize the configuration based on type of streaming connection """
        pass
    
    @abc.abstractmethod
    async def initialize_streaming_connection_configuration(self, **kwargs):
        """ initialize the streaming connection configuration from type of connection """
        pass
    
    ################################################################
    #   weboscket reconnection methods

    def _initialize_websocket_reconnection(self):
        """ Initialize websocket uri """
        self._uri = self._stream_reconnection_config.initialize_websocket_uri(
                                                        self._websocket_endpoint_urls, 
                                                        self._secure)

    def set_next_available_websocket_uri(self):
        """ Set the next available websocket uri """
        #   get next websocket uri and store it
        self._uri = self._stream_reconnection_config.next_websocket_uri()

    def reset_reconnection_config(self):
        """ Reset the reconnection config """
        self._stream_reconnection_config.reset()


    @staticmethod
    def get_streaming_connection_configuration_type(name:str, streaming_connection_config:dict):
        """ get the streaming connection configuration type from given connection name """
        assert(f'{name}.type' in streaming_connection_config)
        return streaming_connection_config[f'{name}.type']
    
    @staticmethod
    async def build_streaming_connection_configuration(session, 
                                                        name:str, 
                                                        platform_url:str, 
                                                        streaming_connection_config:dict,
                                                        **kwargs):
        #   get the type of streaming connection
        connection_type = StreamingConnectionConfiguration.get_streaming_connection_configuration_type(name, streaming_connection_config)

        #   build the streaming connection based on type
        if connection_type == 'service-discovery':
            #   service-discovery type
            streaming_conneciton_config = StreamingConnectionServiceDiscovery(session, name, platform_url,
                                                                                streaming_connection_config)
            
        elif connection_type == 'ads-websocket':
            #   ads-websocket type
            streaming_conneciton_config = StreamingConnectionAdsWebSocket(session, name, platform_url,
                                                                            streaming_connection_config)
        else:
            #   unknown
            raise EnvError(f'ERROR!!! unknown streaming connection type "{connection_type}" from config file.')
        
        #   initialize streaming connection configuration
        await streaming_conneciton_config.initialize_streaming_connection_configuration(**kwargs)

        #   done
        return streaming_conneciton_config

    @staticmethod
    def _build_websocket_uri(websocket_endpoint, secure):
        return '{}://{}/WebSocket'.format('wss' if secure else 'ws', websocket_endpoint)


class StreamingConnectionServiceDiscovery(StreamingConnectionConfiguration):
    """ this class is designed for service-discovery type of streaming connection """

    #   default parameters
    #       service-discovery version
    DefaultServiceDiscoveryVersion = 'v1'
    #       location
    DefaultLocationList = []
    #       data format
    DefaultDataFormat = 'tr_json2'
    #       streaming protocol
    DefaultProtocol = 'OMM'
    
    def __init__(self, session, name:str, platform_url:str, streaming_connection_config:dict):
        StreamingConnectionConfiguration.__init__(self, session, name, platform_url, streaming_connection_config)

        #   list of service-discovery from config file
        assert(self._service_discovery_path is not None)
        assert(self._service_discovery_version is not None)
        assert(self._location_list is not None)
        assert(self._data_format is not None)
        assert(self._protocol is not None)

        #   a service discovery endpoint information
        self._service_discovery_infomation = None

    def _initialize_configuration(self, streaming_connection_config:dict):
        """ initialize the configuration based on type of streaming connection """
        
        #   get the parameters from config file
        #       type
        assert(f'{self._name}.type' in streaming_connection_config)
        connection_type = streaming_connection_config[f'{self._name}.type']
        assert(connection_type == 'service-discovery')

        #       service-discovery path
        assert(f'{self._name}.base-url'         in streaming_connection_config)
        self._service_discovery_path = streaming_connection_config[f'{self._name}.base-url']

        #       service disocvery version
        self._service_discovery_version = streaming_connection_config[f'{self._name}.version'] \
                                        if f'{self._name}.version' in streaming_connection_config \
                                        else self.DefaultServiceDiscoveryVersion

        #       location
        self._location_list = streaming_connection_config[f'{self._name}.locations'] \
                                        if f'{self._name}.locations'  in streaming_connection_config \
                                        else self.DefaultLocationList

        self._data_format = streaming_connection_config[f'{self._name}.format'] \
                                        if f'{self._name}.format' in streaming_connection_config \
                                        else self.DefaultDataFormat

        #       streaming protocol OMM, RDP or etc.
        self._protocol = streaming_connection_config[f'{self._name}.protocol'] \
                                        if f'{self._name}.protocol' in streaming_connection_config \
                                        else self.DefaultProtocol

        #   override platform-url
        self._overide_platform_url = streaming_connection_config[f'{self._name}.platform-url'] \
                                        if f'{self._name}.platform-url' in streaming_connection_config \
                                        else None

    async def initialize_streaming_connection_configuration(self, **kwargs):
        """ initialize the streaming connection configuration from service-discovery configuration
                1. call the service-discovery endpoint to retrieve all streaming websocket endpoints.
                2. filter the streaming websocket based on configuration ie. location
                3. build the streaming connection configuration object 
                    that including uris, authentication token, application id, connection type (secure or not), dacs position
        """
        assert('dacs_position' in kwargs)
        assert('dacs_application_id' in kwargs)

        #   retrieve the streaming websocket endpoints from service discovery endpoint
        await self._retrieve_streaming_websocket_endpoint()
        assert(self._service_discovery_infomation is not None)

        #   get the weboscket authority list by location, transportation and format
        self._websocket_endpoint_urls = self._service_discovery_infomation.get_websocket_authority_list_by_location(location_list=self._location_list, 
                                                                                                                        data_format=self._data_format)
        #   connection parameters
        self._dacs_application_id = kwargs['dacs_application_id']
        self._dacs_position = kwargs["dacs_position"]

        #   do intialize the reconenction configuration
        self._initialize_websocket_reconnection()

    def _service_discovery_infomation_cls(self):
        """ get the service discovery information class based on the service discovery version """
        #   choose the service discovery information based on version
        if self._service_discovery_version == 'beta1':
            #   beta1
            return ServiceDiscoveryBeta1Information
        elif self._service_discovery_version == 'v1':
            #   v1
            return ServiceDiscoveryV1Information
        else:
            #   unknown service discovery version or unsupported version
            #       raise an error
            raise EnvError(-1, f'ERROR!!! unknown or unsupported service discovery version "{self._service_discovery_version}"')

    async def _retrieve_streaming_websocket_endpoint(self):
        """ retrieve a list of streaming websocket endpoint from the service-discovery """
        #   build a service discovery endpoint
        platform_url = self._platform_url
        if self._overide_platform_url is not None:
            #   this service discovery override platform-url
            platform_url = self._overide_platform_url

        #   build service discovery uri
        service_discovery_uri = urllib.parse.urljoin(platform_url, self._service_discovery_path)
        assert(service_discovery_uri is not None)
        self._session.log(logging.DEBUG, f'retrieve_streaming_websocket_endpoint(service_discovery_uri={service_discovery_uri})')

        #   send a http request to service discovery endpoint to get a streaming endpoint
        response = None
        try:
            #   make a request to the discovery endpoint
            response = await self._session.http_request_async(service_discovery_uri, method='GET')
        except Exception as e:
            raise EnvError(-1, f"{e!r}")
        
        assert(response is not None)
        self._session.log(logging.DEBUG, f'      service discovery endpoint response: {response.text}')
        
        #   check response status from discovery endpoint
        if response.status_code != requests.codes.ok:
            # self._status = Session.EventCode.StreamDisconnected
            raise EnvError(response.status_code, response.text)

        #   extract and build the endpoint services from discovery endpoint response
        discovery_endpoint_response_json = response.json()
        service_discovery_infomation_cls = self._service_discovery_infomation_cls()
        #   build the service discovery information object
        self._service_discovery_infomation = service_discovery_infomation_cls(self._name, discovery_endpoint_response_json)


class StreamingConnectionAdsWebSocket(StreamingConnectionConfiguration):
    """ this class is designed for ads-websocket type of streaming connection """
   
    #   default parameters
    #       secure connection
    DefaultSecureConnection = False
    #       streaming protocol
    DefaultProtocol = 'OMM'
    #       dacs username
    DefaultDacsUsername = ""
    #       dacs application id
    DefaultDacsApplicationId = 256

    def __init__(self, session, name:str, platform_url:str, streaming_connection_config:dict):
        StreamingConnectionConfiguration.__init__(self, session, name, platform_url, streaming_connection_config)
        
        assert(self._websocket_url is not None)
        assert(self._protocol is not None)
        assert(self._secure is not None)

    def _initialize_configuration(self, streaming_connection_config:dict):
        """ initialize the configuration based on type of streaming connection """
        #   get the parameters from config file
        #       type
        assert(f'{self._name}.type' in streaming_connection_config)
        connection_type = streaming_connection_config[f'{self._name}.type']
        assert(connection_type == 'ads-websocket')

        #       websocket-url
        assert(f'{self._name}.websocket-url' in streaming_connection_config)
        self._websocket_url = streaming_connection_config[f'{self._name}.websocket-url']

         #       streaming protocol OMM, RDP or etc.
        self._protocol = streaming_connection_config[f'{self._name}.protocol'] \
                                        if f'{self._name}.protocol' in streaming_connection_config \
                                        else self.DefaultProtocol

         #       streaming secure connection (using ssl or not?)
        self._secure = streaming_connection_config[f'{self._name}.secure'] \
                                        if f'{self._name}.secure' in streaming_connection_config \
                                        else self.DefaultSecureConnection

        #       dacs username
        self._dacs_username = streaming_connection_config[f'{self._name}.dacs_username'] \
                                        if f'{self._name}.dacs_username' in streaming_connection_config \
                                        else self.DefaultDacsUsername
        #       dacs application id
        self._dacs_username = streaming_connection_config[f'{self._name}.dacs_username'] \
                                        if f'{self._name}.dacs_username' in streaming_connection_config \
                                        else self.DefaultDacsApplicationId

    async def initialize_streaming_connection_configuration(self, **kwargs):
        """ initialize the streaming connection configuration from type of connection """

        assert('dacs_username' in kwargs)
        assert('dacs_position' in kwargs)
        assert('dacs_application_id' in kwargs)

        #   get the weboscket authority list by location, transportation and format
        self._websocket_endpoint_urls = [self._websocket_url,] 
        
        #   connection parameters
        if 'dacs_username' in kwargs and kwargs['dacs_username'] is not None:
            self._dacs_username = kwargs['dacs_username']
        if 'dacs_application_id' in kwargs and kwargs['dacs_application_id'] is not None:
            self._dacs_application_id = kwargs['dacs_application_id']
        if 'dacs_position' in kwargs and kwargs['dacs_position'] is not None:
            self._dacs_position = kwargs['dacs_position']

        #   do intialize the reconnection configuration
        self._initialize_websocket_reconnection()