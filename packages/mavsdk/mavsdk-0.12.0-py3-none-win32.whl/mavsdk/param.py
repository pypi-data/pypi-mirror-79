# -*- coding: utf-8 -*-
# DO NOT EDIT! This file is auto-generated from
# https://github.com/mavlink/MAVSDK-Python/tree/master/other/templates/py
from ._base import AsyncBase
from . import param_pb2, param_pb2_grpc
from enum import Enum


class ParamResult:
    """
     Result type.

     Parameters
     ----------
     result : Result
          Result enum value

     result_str : std::string
          Human-readable English string describing the result

     """

    
    
    class Result(Enum):
        """
         Possible results returned for param requests.

         Values
         ------
         UNKNOWN
              Unknown result

         SUCCESS
              Request succeeded

         TIMEOUT
              Request timed out

         CONNECTION_ERROR
              Connection error

         WRONG_TYPE
              Wrong type

         PARAM_NAME_TOO_LONG
              Parameter name too long (> 16)

         """

        
        UNKNOWN = 0
        SUCCESS = 1
        TIMEOUT = 2
        CONNECTION_ERROR = 3
        WRONG_TYPE = 4
        PARAM_NAME_TOO_LONG = 5

        def translate_to_rpc(self):
            if self == ParamResult.Result.UNKNOWN:
                return param_pb2.ParamResult.RESULT_UNKNOWN
            if self == ParamResult.Result.SUCCESS:
                return param_pb2.ParamResult.RESULT_SUCCESS
            if self == ParamResult.Result.TIMEOUT:
                return param_pb2.ParamResult.RESULT_TIMEOUT
            if self == ParamResult.Result.CONNECTION_ERROR:
                return param_pb2.ParamResult.RESULT_CONNECTION_ERROR
            if self == ParamResult.Result.WRONG_TYPE:
                return param_pb2.ParamResult.RESULT_WRONG_TYPE
            if self == ParamResult.Result.PARAM_NAME_TOO_LONG:
                return param_pb2.ParamResult.RESULT_PARAM_NAME_TOO_LONG

        @staticmethod
        def translate_from_rpc(rpc_enum_value):
            """ Parses a gRPC response """
            if rpc_enum_value == param_pb2.ParamResult.RESULT_UNKNOWN:
                return ParamResult.Result.UNKNOWN
            if rpc_enum_value == param_pb2.ParamResult.RESULT_SUCCESS:
                return ParamResult.Result.SUCCESS
            if rpc_enum_value == param_pb2.ParamResult.RESULT_TIMEOUT:
                return ParamResult.Result.TIMEOUT
            if rpc_enum_value == param_pb2.ParamResult.RESULT_CONNECTION_ERROR:
                return ParamResult.Result.CONNECTION_ERROR
            if rpc_enum_value == param_pb2.ParamResult.RESULT_WRONG_TYPE:
                return ParamResult.Result.WRONG_TYPE
            if rpc_enum_value == param_pb2.ParamResult.RESULT_PARAM_NAME_TOO_LONG:
                return ParamResult.Result.PARAM_NAME_TOO_LONG

        def __str__(self):
            return self.name
    

    def __init__(
            self,
            result,
            result_str):
        """ Initializes the ParamResult object """
        self.result = result
        self.result_str = result_str

    def __equals__(self, to_compare):
        """ Checks if two ParamResult are the same """
        try:
            # Try to compare - this likely fails when it is compared to a non
            # ParamResult object
            return \
                (self.result == to_compare.result) and \
                (self.result_str == to_compare.result_str)

        except AttributeError:
            return False

    def __str__(self):
        """ ParamResult in string representation """
        struct_repr = ", ".join([
                "result: " + str(self.result),
                "result_str: " + str(self.result_str)
                ])

        return f"ParamResult: [{struct_repr}]"

    @staticmethod
    def translate_from_rpc(rpcParamResult):
        """ Translates a gRPC struct to the SDK equivalent """
        return ParamResult(
                
                ParamResult.Result.translate_from_rpc(rpcParamResult.result),
                
                
                rpcParamResult.result_str
                )

    def translate_to_rpc(self, rpcParamResult):
        """ Translates this SDK object into its gRPC equivalent """

        
        
            
        rpcParamResult.result = self.result.translate_to_rpc()
            
        
        
        
            
        rpcParamResult.result_str = self.result_str
            
        
        



class ParamError(Exception):
    """ Raised when a ParamResult is a fail code """

    def __init__(self, result, origin, *params):
        self._result = result
        self._origin = origin
        self._params = params

    def __str__(self):
        return f"{self._result.result}: '{self._result.result_str}'; origin: {self._origin}; params: {self._params}"


class Param(AsyncBase):
    """
     Provide raw access to get and set parameters.

     Generated by dcsdkgen - MAVSDK Param API
    """

    # Plugin name
    name = "Param"

    def _setup_stub(self, channel):
        """ Setups the api stub """
        self._stub = param_pb2_grpc.ParamServiceStub(channel)

    
    def _extract_result(self, response):
        """ Returns the response status and description """
        return ParamResult.translate_from_rpc(response.param_result)
    

    async def get_param_int(self, name):
        """
         Get an int parameter.

         If the type is wrong, the result will be `WRONG_TYPE`.

         Parameters
         ----------
         name : std::string
              Name of the parameter

         Returns
         -------
         value : int32_t
              Value of the requested parameter

         Raises
         ------
         ParamError
             If the request fails. The error contains the reason for the failure.
        """

        request = param_pb2.GetParamIntRequest()
        
            
        request.name = name
            
        response = await self._stub.GetParamInt(request)

        
        result = self._extract_result(response)

        if result.result is not ParamResult.Result.SUCCESS:
            raise ParamError(result, "get_param_int()", name)
        

        return response.value
        

    async def set_param_int(self, name, value):
        """
         Set an int parameter.

         If the type is wrong, the result will be `WRONG_TYPE`.

         Parameters
         ----------
         name : std::string
              Name of the parameter to set

         value : int32_t
              Value the parameter should be set to

         Raises
         ------
         ParamError
             If the request fails. The error contains the reason for the failure.
        """

        request = param_pb2.SetParamIntRequest()
        request.name = name
        request.value = value
        response = await self._stub.SetParamInt(request)

        
        result = self._extract_result(response)

        if result.result is not ParamResult.Result.SUCCESS:
            raise ParamError(result, "set_param_int()", name, value)
        

    async def get_param_float(self, name):
        """
         Get a float parameter.

         If the type is wrong, the result will be `WRONG_TYPE`.

         Parameters
         ----------
         name : std::string
              Name of the parameter

         Returns
         -------
         value : float
              Value of the requested parameter

         Raises
         ------
         ParamError
             If the request fails. The error contains the reason for the failure.
        """

        request = param_pb2.GetParamFloatRequest()
        
            
        request.name = name
            
        response = await self._stub.GetParamFloat(request)

        
        result = self._extract_result(response)

        if result.result is not ParamResult.Result.SUCCESS:
            raise ParamError(result, "get_param_float()", name)
        

        return response.value
        

    async def set_param_float(self, name, value):
        """
         Set a float parameter.

         If the type is wrong, the result will be `WRONG_TYPE`.

         Parameters
         ----------
         name : std::string
              Name of the parameter to set

         value : float
              Value the parameter should be set to

         Raises
         ------
         ParamError
             If the request fails. The error contains the reason for the failure.
        """

        request = param_pb2.SetParamFloatRequest()
        request.name = name
        request.value = value
        response = await self._stub.SetParamFloat(request)

        
        result = self._extract_result(response)

        if result.result is not ParamResult.Result.SUCCESS:
            raise ParamError(result, "set_param_float()", name, value)
        