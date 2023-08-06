# coding: utf-8

__all__ = ['get_chain', 'get_chain_async']

###############################################################
#
#   STANDARD IMPORTS
#


###############################################################
#
#   REFINITIV IMPORTS
#

from .Chain import Chain


###############################################################
#
#   LOCAL IMPORTS
#

###############################################################
#
#   FUNCTIONS
#

def get_chain(universe, on_response=None, session=None):
    from refinitiv.dataplatform.factory.content_factory import ContentFactory

    response = Chain.decode(universe=universe, session=session, on_response=on_response)

    ContentFactory._last_result = response
    if response.is_success and response.data and response.data.df is not None:
        return response.data.df
    else:
        ContentFactory._last_error_status = response.status
        return None


async def get_chain_async(universe, on_response=None, session=None):
    from refinitiv.dataplatform.factory.content_factory import ContentFactory

    response = await Chain.decode_async(universe=universe, session=session, on_response=on_response)

    ContentFactory._last_result = response
    if response.is_success and response.data and response.data.df is not None:
        return response.data.df
    else:
        ContentFactory._last_error_status = response.status
        return None
