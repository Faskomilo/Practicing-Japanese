"""
A file that contains the Utils class.
"""
import yaml

class Utils():
    """
    A class for diverse standalone util functions.
    """

    @staticmethod
    def read_config() -> dict:
        """
        Obtains the information of a yaml config file.

        Returns:
            dict: the dictionary with the yaml config file contents.
        """
        with open("config.yaml", "r") as file:
            config = yaml.safe_load(file)
        return config
    
    @staticmethod
    def check_if_in_config(config: dict, path: str):
        """
        Checks if a variable path exists in the config file.

        Args:
            config (dict): A dictionary of a config yaml file.
            path (str): The path of a variable, such as path.to.variable .
        """
        path_list = path.split(".")
        config = config
        for element in path_list:
            try:
                config[element]
            except:
                print(f"{element} missing in config, the needed " +
                      f"variable path is {path}, we recomend to copy the " +
                      "example_config.yaml file in the project root as " +
                      "config.yaml in the same directory")
                exit()