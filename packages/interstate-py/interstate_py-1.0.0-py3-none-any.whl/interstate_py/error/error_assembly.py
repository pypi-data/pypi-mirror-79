import json
import sys
import traceback
from typing import List

from interstate_py.interstate_message import InterstateWireMessage, InterstateWireMessageType
from interstate_py.multiplex_message import MultiplexMessage


class InterstateError:
    def __init__(self, error_type: str, error_message: str, stacktrace: List[str]):
        self._error_type = error_type
        self._error_message = error_message
        self._stacktrace = stacktrace

    @property
    def error_type(self):
        return self._error_type

    @property
    def error_message(self):
        return self._error_message

    @property
    def stacktrace(self):
        return self._stacktrace

    def __repr__(self) -> str:
        return "InterstateError(type={}, message={}, stacktrace={})".format(self._error_type, self._error_message, self._stacktrace)


class ErrorAssembly:

    @staticmethod
    def to_error(e: Exception) -> InterstateError:
        return InterstateError(
            e.__class__.__name__,
            ErrorAssembly.exc_message(e),
            ErrorAssembly.get_stacktrace(50))

    @staticmethod
    def to_on_error(multiplex_message: MultiplexMessage) -> InterstateWireMessage:
        """
           Converts multiplex messages that contains exceptions to an on_error interstate message carrying the exception
        """
        if multiplex_message.type != InterstateWireMessageType.ERROR:
            raise Exception("Only error message can be converted")

        error_message = multiplex_message.payload

        return InterstateWireMessage(multiplex_message.identity.encode(), InterstateWireMessageType.header("error"),
                                     json.dumps({
                                         "errorType": error_message.error_type,
                                         "errorMessage": error_message.error_message,
                                         "stacktrace": error_message.stacktrace
                                     }).encode())

    @staticmethod
    def exc_message(exception: Exception) -> str:
        """
        Extracts the message from the given exception. Some exceptions carry the message within a 'message' field while
        others does not.
        :param exception:
        :return:
        """
        if hasattr(exception, 'message'):
            return exception.message
        else:
            return repr(exception)

    @staticmethod
    def get_stacktrace(limit: int) -> List[str]:
        (_, _, s) = sys.exc_info()
        return traceback.format_list(traceback.extract_tb(s, limit=limit))
