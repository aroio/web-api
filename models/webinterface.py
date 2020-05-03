from pydantic import BaseModel

class WebinterfaceConfig(BaseModel):
    display_rotate: bool = False
    dark_mode: bool = False
    initial_setup: bool = True
    advanced_configuration: bool = False