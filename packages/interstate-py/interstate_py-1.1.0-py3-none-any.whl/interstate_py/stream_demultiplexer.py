import asyncio
from asyncio import Queue
from concurrent.futures.thread import ThreadPoolExecutor

import janus

from interstate_py.connection_agent import ConnectionAgentBase
from interstate_py.control.worker_task import AIOWorkerTask
from interstate_py.error.error_assembly import ErrorAssembly
from interstate_py.interstate_message import InterstateWireMessageType
from interstate_py.log_factory import LogFactory
from interstate_py.multiplex_message import MultiplexMessage
from interstate_py.serialization.serialization import Serialization
from interstate_py.stream_connection import StreamConnection


class StreamDemultiplexer(AIOWorkerTask):
    """
    Demultiplexes a messages by extracting its identity and calling the according emitter method on
    the corresponding connection provided by the connection agent.
    """
    _log = LogFactory.get_logger(__name__)

    def __init__(self, raw_inbound_queue: Queue,
                 outbound_queue: janus.Queue,
                 con_agent: ConnectionAgentBase,
                 serialization: Serialization):  # TODO: interceptor
        super().__init__()
        self._raw_inbound_queue = raw_inbound_queue
        self._outbound_queue = outbound_queue
        self._con_agent = con_agent
        self._serialization = serialization

    async def do_work(self):
        message = await self._raw_inbound_queue.get()
        identity = message.identity.decode()
        connection = self._con_agent.get(identity)

        def _send(connection: StreamConnection, payload):
            self._log.debug("Sending payload to subject")
            connection.inbound_stream().on_next(payload)
            self._log.debug("Payload sent to subject")

        if message.type == InterstateWireMessageType.NEXT:
            self._log.debug("[IN][NEXT] - {}".format(message))
            try:
                deserialized_payload = self._serialization.deserialize(message.payload)
                asyncio.get_event_loop().run_in_executor(ThreadPoolExecutor(5), #TODO: configurable
                                                               _send,
                                                               connection,
                                                               deserialized_payload)
            except Exception as e:
                self._log.warn("[IN][NEXT] - Could not deserialize incoming message: %s", ErrorAssembly.exc_message(e))
                await self._outbound_queue.async_q.put(
                    MultiplexMessage(message.identity.decode(), InterstateWireMessageType.ERROR,
                                     ErrorAssembly.to_error(ErrorAssembly.DESERIALIZATION_ERROR_TYPE,
                                                            e)))
        elif message.type == InterstateWireMessageType.ERROR:
            self._log.warn("[IN][ERROR] - {}".format(message))
            connection.inbound_stream().on_error(Exception("Error"))
            connection.close_inbound()
        elif message.type == InterstateWireMessageType.COMPLETE:
            self._log.debug("[IN][COMPLETED] - {}".format(message))
            connection.inbound_stream().on_completed()
            connection.close_inbound()
        elif message.type == InterstateWireMessageType.PING:
            # TODO: find a better way via interceptors or another mechanism
            self._log.debug("[IN][PING] - {}".format(message))
            await self._outbound_queue.async_q.put(MultiplexMessage(identity, InterstateWireMessageType.PONG, "pong".encode()))
        else:
            self._log.warn("Can not handle message: {}".format(message))

        self._raw_inbound_queue.task_done()
