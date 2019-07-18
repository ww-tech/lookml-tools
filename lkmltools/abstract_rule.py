from abc import ABC, abstractmethod

class AbstractRule(ABC):
    """Abstract rule that can take a JSON configuration object"""

    def __init__(self, config_dict=None):
        """set the config_dict, if any
        
        Args:
            config_dict (dict): dictionary configuration from the config file

        """
        if config_dict:
            assert isinstance(config_dict, dict)
        self.config_dict = config_dict

    def has_key(self, key):
        """does the config dictionary have a key 'key'?

        Returns:
            response (bool): whether there is a configuration dictionary and key is present

        """
        if self.config_dict:
            return key in self.config_dict
        return False 
    
    def config_for_key(self, key):
        if self.config_dict and key in self.config_dict:
            return self.config_dict[key]
        return None