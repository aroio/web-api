from models.aroio import Aroio, NetworkConfig, ConvolverConfig
import logging
import json

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


    def sync(
        self,
        aroio: Aroio=None,
        network_config: NetworkConfig=None,
        convolver_config: ConvolverConfig=None):
        db = self.load_aroio()
        if convolver_config is not None:
            db.configuration.convolver = convolver_config
        if network_config is not None:
            db.configuration.network = network_config
        if aroio is not None:
            db = aroio
        
        with open(self.aroio_path, 'w') as f:
            f.write(json.dumps(db.dict()))
            f.close()
        return db


    def load_translations(self, lang: str):
        """Loading the aroio translations from system"""
        translation = {
            "DE": self.translation_path + "messages.de.yml",
            "EN": self.translation_path + "messages.en.yml"
        }[lang]
    
        with open(translation, "r") as yml_file:
            return yaml.load(yml_file)
