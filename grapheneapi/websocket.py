import ssl
import json
import logging
import websocket
from .rpc import Rpc

log = logging.getLogger(__name__)


class Websocket(Rpc):

    def connect(self):
        log.debug("Trying to connect to node %s" % self.url)
        if self.url[:3] == "wss":
            ssl_defaults = ssl.get_default_verify_paths()
            sslopt_ca_certs = {'ca_certs': ssl_defaults.cafile}
            self.ws = websocket.WebSocket(sslopt=sslopt_ca_certs)
        else:  # pragma: no cover
            self.ws = websocket.WebSocket()

        self.ws.connect(self.url)
        if self.user and self.password:
            self.login(self.user, self.password, api_id=1)

    def disconnect(self):
        if self.ws:
            try:
                self.ws.close()
                self.ws = None
            except Exception:  # pragma: no cover
                pass

    """ RPC Calls
    """
    def rpcexec(self, payload):
        """ Execute a call by sending the payload

            :param json payload: Payload data
            :raises ValueError: if the server does not respond in proper JSON
                format
        """
        if not self.ws:  # pragma: no cover
            self.connect()

        log.debug(json.dumps(payload))
        self.ws.send(
            json.dumps(payload, ensure_ascii=False).encode('utf8')
        )
        return self.ws.recv()
