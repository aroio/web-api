from models import (
    Aroio,
    Configuration,
    NetworkConfig,
    SystemConfig,
    StreamingConfig,
    AudioConfig,
    ConvolverConfig,
    Filter
)
from typing import List
import json
import yaml

# Dev
databasePath = "./aroio_db.json";
translationsPath = "./translations/";

# Prod
# databasePath = "/tmp/aroio_db.json";
# translationsPath = "/opt/api/translations/";


class DataSource:

    def __init__(self, path: str = databasePath, translation_path: str = translationsPath):
        self.aroio_path = path
        self.translation_path = translation_path

    def load_aroio(self) -> Aroio:
        """Reads data of Aroio from userconfig"""
        try:
            with open(self.aroio_path) as f:
                aroio_db = json.load(f)
                return Aroio(**aroio_db)
        except IOError:
            print("Database not accessable, generate Database.")
            aroio = Aroio()
            # Save aroio as the initial database model
            self.save(aroio=aroio)
            return aroio

    def sync(self,
             aroio: Aroio = None,
             configuration: Configuration = None,
             network_config: NetworkConfig = None,
             system_config: SystemConfig = None,
             streaming_config: StreamingConfig = None,
             audio_config: AudioConfig = None,
             convolver_config: ConvolverConfig = None,
             filters: List[Filter] = None):
        """Syncing of entities.
        Updating Aroio entities by just passing as a parameter. E.g.:
        ```
        aroio = Aroio()
        ds = DataSource()
        ds.sync(aroio=Aroio)
        ```

        The more detailed settings would override the more general settings.
        E.g. a SystemConfig would override the SystemConfig set by the Configuration object.
        """
        db = self.load_aroio()

        if aroio is not None:
            db = aroio
        if configuration is not None:
            db.configuration = configuration
        if network_config is not None:
            db.configuration.network = network_config
        if system_config is not None:
            db.configuration.system = system_config
        if streaming_config is not None:
            db.configuration.streaming = streaming_config
        if audio_config is not None:
            db.configuration.audio = audio_config
        if convolver_config is not None:
            db.configuration.convolver = convolver_config
        if filters is not None:
            db.configuration.convolver.filters = filters

        self.save(aroio=db)

        return db

    def save(self, aroio: Aroio):
        """Saving an aroio object"""
        with open(self.aroio_path, 'w') as f:
            f.write(json.dumps(aroio.dict()))
            f.close()

    def load_translations(self, lang: str):
        """
        Loading the aroio translations from system. Currently only english 
        and german is supported. For required translation pass in intials 
        of required language. Initials can be passed in either way uppercase 
        and lowercase. E.g. for english translation `EN` or `en` is possible.
        """
        translation = {
            "DE": self.translation_path + "messages.de.yml",
            "EN": self.translation_path + "messages.en.yml"
        }[lang.upper()]

        with open(translation, "r") as yml_file:
            return yaml.safe_load(yml_file)


# Import this shit Singleton style!
datasource = DataSource()
