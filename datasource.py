import json
import logging

import yaml

from models.aroio import Aroio, ConvolverConfig, NetworkConfig


class DataSource:

    def __init__(self, path: str="./aroio_db.json", translation_path: str="./translations/"):
        self.aroio_path = path
        self.translation_path = translation_path


    def load_aroio(self) -> Aroio:
        """Reads data of Aroio from userconfig"""
        try:
            with open(self.aroio_path, "r") as json_file:
                return Aroio.create_from_json(json_file)
        except IOError:
            logging.info("Database not accessible, generate Database.")
            return self.sync_aroio(Aroio.initial_aroio())


    def sync_aroio(self, aroio: Aroio) -> Aroio:
        """Syncing an Aroio entity"""
        with open(self.aroio_path, 'w+') as db:
            db.write(json.dumps(aroio.dict()))
            db.close()
        return aroio


    def sync_network_config(self, network_config: NetworkConfig):
        """Syncing a NetworkConfig"""
        aroio = self.load_aroio()
        aroio.configuration.network = network_config
        self.sync_aroio(aroio=aroio)


    def sync_convolver_config(self, convolver: ConvolverConfig):
        """Syncing a ConvolverConfig"""
        aroio = self.load_aroio()
        aroio.configuration.convolver = convolver
        self.sync_aroio(aroio=aroio)


    def load_translations(self, lang: str):
        """Loading the aroio translations from system"""
        translation = {
            "DE": self.translation_path + "messages.de.yml",
            "EN": self.translation_path + "messages.en.yml"
        }[lang]
    
        with open(translation, "r") as yml_file:
            return yaml.load(yml_file)
