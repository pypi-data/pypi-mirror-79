# coding: utf8

__all__ = ["Fundamental"]

from enum import Enum, unique

from refinitiv.dataplatform.delivery.data import Endpoint
from refinitiv.dataplatform.tools._common import is_all_same_type
from ._fundamental_definition import FundamentalDefinition


class Fundamental(Endpoint):

    def __init__(self, session=None, on_response=None):
        from refinitiv.dataplatform.legacy.tools import DefaultSession
        session = session or DefaultSession.get_default_session()
        session._env.raise_if_not_available('fundamental')
        _url = session._env.get_url_or_raise_error('fundamental.datagrid')
        super().__init__(
            session,
            _url,
            on_response=on_response,
            service_class=FundamentalDefinition
        )

    def _run_until_complete(self, future):
        return self.session._loop.run_until_complete(future)

    @staticmethod
    def get_data(universe,
             fields,
             parameters=None,
             field_name=None,
             on_response=None,
             closure=None,
             session=None
             ):
        fundamental = Fundamental(session=session, on_response=on_response)
        result = fundamental._get_data(universe=universe,
                                       fields=fields,
                                       parameters=parameters,
                                       field_name=field_name,
                                       closure=None,
                                       session=None
                                       )
        return result

    def _get_data(self,
                  universe,
                  fields,
                  parameters=None,
                  field_name=None,
                  closure=None,
                  session=None):
        """
        :param universe: list    The list of RICs
        :param fields: list      List of fundamental field names
        :param parameters
        :param closure:str
        :param session:Session
        :return:Response
        """
        result = self._run_until_complete(self._get_data_async(
            universe=universe,
            fields=fields,
            parameters=parameters,
            field_name=field_name,
            outputs=outputs,
            closure=closure
        ))
        return result

    async def _get_data_async(self,
                              universe,
                              fields,
                              parameters=None,
                              field_names=None,
                              closure=None,
                              session=None):

        from refinitiv.dataplatform.legacy.tools import DefaultSession

        logger = DefaultSession.get_default_session().logger()

        check_for_string_or_list_of_strings(universe, 'universe')
        universe = build_list(universe, 'universe')
        universe = [value.upper() if value.islower() else value for value in universe]

        if parameters:
            parameters = build_dictionary(parameters, 'parameters')

        if field_names is None:
            field_names = False

        fields = Fundamental._parse_fields(fields)
        fields_for_request = []
        for f in fields:
            keys = list(f.keys())
            if len(keys) != 1:
                with 'get_data error: The field dictionary should contain a single key which is the field name' as msg:
                    logger.error(msg)
                    raise ValueError(msg)
            name = list(f.keys())[0]
            field_info = f[name]
            if type(field_info) != dict:
                with 'get_data error: The parameters for the file {} should be passed in a dict'.format(
                        name) as error_msg:
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            field = {'name': name}
            if 'sort_dir' in list(field_info.keys()):
                field['sort'] = field_info['sort_dir']
            if 'sort_priority' in list(field_info.keys()):
                field['sortPriority'] = field_info['sort_priority']
            if 'params' in list(field_info.keys()):
                field['parameters'] = field_info['params']
            fields_for_request.append(field)

        payload = {'instruments': instruments, 'fields': fields_for_request}
        if parameters:
            payload.update({'parameters': parameters})

        response = await self.send_request_async(Endpoint.RequestMethod.POST,
                                path_parameters=path_parameters,
                                query_parameters=_query_parameters,
                                closure=closure)
        if _result and not _result.is_success:
            self.session.log(1, f'Fundamental historical_pricing request failed: {_result.status}')
        return response

        return get_data_frame(result, field_name)

    def _on_response(self, endpoint, data):

        self._data = data

        if self._on_response_cb:
            _result = FundamentalDefinition(data._response, _convert_fundamental_json_to_pandas)
            if not _result.is_success:
                self.session.log(1, f'Fundamental data request failed: {_result.status}')
            self._on_response_cb(self, _result)

    @staticmethod
    def _parse_fields(fields):
        if is_string_type(fields):
            return [{fields: {}}]

        logger = DefaultSession.get_default_session().logger()
        if type(fields) == dict:
            if len(fields) == 0:
                with 'get_data error: fields list must not be empty' as error_msg:
                    logger.error(error_msg)
                    raise ValueError(error_msg)
            return [fields]
        field_list = []
        if type(fields) == list:
            if len(fields) == 0:
                with 'get_data error: fields list must not be empty' as error_msg:
                    logger.error(error_msg)
                    raise ValueError(error_msg)
            for f in fields:
                if is_string_type(f):
                    field_list.append({f: {}})
                elif type(f) == dict:
                    field_list.append(f)
                else:
                    error_msg = 'get_data error: the fields should be of type string or dictionary'
                    DefaultSession.get_default_session().logger().error(error_msg)
                    raise ValueError(error_msg)
            return field_list

        error_msg = 'get_data error: the field parameter should be a string, a dictionary , or a list of strings|dictionaries'
        DefaultSession.get_default_session().logger().error(error_msg)
        raise ValueError(error_msg)

    @staticmethod
    def _get_data_value(value):
        if is_string_type(value):
            return value
        elif value is dict:
            return value['value']
        else:
            return value


def _convert_fundamental_json_to_pandas(json_fundamental_data):
    _fields = [field['name'] for field in json_esg_data['headers']]
    fundamental_dataframe = None
    _data = json_fundamental_data['data']
    if _data:
        # build numpy array with all datapoints
        _numpy_array = numpy.array(_data)
        fundamental_dataframe = pd.DataFrame(_numpy_array, columns=_fields)
        if not fundamental_dataframe.empty:
            fundamental_dataframe = fundamental_dataframe.convert_dtypes()  # convert_string=False)
    else:
        fundamental_dataframe = pd.DataFrame([], columns=_fields)

    return fundamental_dataframe

    # @staticmethod
    # def _get_data_frame(data_dict, field_name=False):
    #     if field_name:
    #         headers = [header.get('field', header.get('displayName')) for header in data_dict['headers'][0]]
    #     else:
    #         headers = [header['displayName'] for header in data_dict['headers'][0]]
    #     data = numpy.array([[Fundamental._get_data_value(value) for value in row] for row in data_dict['data']])
    #     df = pd.DataFrame(data, columns=headers)
    #     df = df.convert_dtypes()  # convert_string=False)
    #     errors = get_json_value(data_dict, 'error')
    #     return df, errors




