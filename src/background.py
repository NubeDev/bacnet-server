import logging
from threading import Thread

from flask import current_app
from mrb.brige import MqttRestBridge

from .setting import AppSetting

logger = logging.getLogger(__name__)


class FlaskThread(Thread):
    """
    To make every new thread behinds Flask app context.
    Maybe using another lightweight solution but richer: APScheduler <https://github.com/agronholm/apscheduler>
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = current_app._get_current_object()

    def run(self):
        with self.app.app_context():
            super().run()


class Background:
    @staticmethod
    def run():
        from src.bacnet_server import BACServer
        from src.mqtt import MqttClient
        setting: AppSetting = current_app.config[AppSetting.FLASK_KEY]
        logger.info("Running Background Task...")
        if setting.mqtt.enabled:
            FlaskThread(target=MqttClient().start, daemon=True, kwargs={'config': setting.mqtt}).start()

        if setting.bacnet.enabled:
            FlaskThread(target=BACServer().start_bac, daemon=True, kwargs={'config': setting.bacnet}).start()

        if setting.mqtt_rest_bridge_setting.enabled:
            FlaskThread(target=MqttRestBridge(port=setting.port, identifier=setting.identifier, prod=setting.prod,
                                              mqtt_setting=setting.mqtt_rest_bridge_setting,
                                              callback=Background.sync_points_values).start, daemon=True).start()

    @staticmethod
    def sync_points_values():
        from .bacnet_server.models.model_point_store import BACnetPointStoreModel
        BACnetPointStoreModel.sync_points_values()
