from kombu import Connection
import logging
from applauncher.kernel import ConfigurationReadyEvent, KernelShutdownEvent


class AmqpBundle(object):

    def __init__(self):
        self.logger = logging.getLogger("amqp_bundle")
        self.config_mapping = {
            "amqp": {
                "uri": None,
                "autodisconnect": False,
                "heartbeat": 0,
            }
        }
        self.autodisconnect = None

        self.event_listeners = [
            (ConfigurationReadyEvent, self.configuration_ready),
            (KernelShutdownEvent, self.kernel_shutdown),
        ]

        self.connection = Connection()
        self.injection_bindings = {Connection: self.connection}

    def kernel_shutdown(self, event):
        if self.autodisconnect:
            self.logger.info("Disconnecting...")
            self.connection.release()
            self.logger.info("Disconnected")

    def configuration_ready(self, event):
        c = event.configuration.amqp
        self.autodisconnect = c.autodisconnect
        # First connect the topic manager to avoid lose messages
        self.connection.__init__(c.uri, heartbeat=c.heartbeat)
        self.connection.connect()
        self.logger.info("Connected")
