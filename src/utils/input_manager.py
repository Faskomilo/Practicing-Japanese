"""
A file that contains a the Input_Manager class.
"""

from typing import Union, Tuple

# All the valid types so far for inputs.
valid_types = Union[str,int]

class Input_Manager():
    """
    Class for managing inputs.
    """
    def __init__(self, config) -> None:
        """
        Gets system.input_tries config value.

        Args:
            config (dict): A dictionary of a config yaml file.
        """
        self._max_tries_ = config["system"]["input_tries"]

    def ask_input(self,
                  message: str,
                  expected_type: valid_types,
                  options: list = []
                  ) -> valid_types:
        """
        A function that asks for an input, with a certain quantity of tries
        in case of errors, and handles empty values, non accepted input types
        and whether the input belongs to a set of options.

        Args:
            message (str): A message to ask the input with.
            expected_type (valid_types): The type that the input should be.
            options (list, optional): A list of options if expecting an
                specific input from a set. Defaults to [].

        Raises:
            ValueError: If the tries limit has been reached.

        Returns:
            valid_types: The option formatted to the expected type.
        """
        self._tries_ = self._max_tries_
        valid_input = False

        while self._tries_ >= 0 and not valid_input:
            given_input = input(message)
            if given_input in [None, ""]:
                print(f"Error, insert a value\nTries left: {self._tries_}\n")
                self._tries_ -= 1
                continue
            valid_given_type, given_input = self.__check_input_type(
                given_input,
                expected_type)
            if not valid_given_type:
                self._tries_ -= 1
                continue
            if not self.__check_options_complience(given_input, options):
                self._tries_ -= 1
                continue
            valid_input = True
        if self._tries_ < 0:
            print("Error, max tries reached")
            exit()
        return given_input

    def __check_input_type(self,
                           given_input_string: str,
                           expected_type: valid_types,
                           ) -> Tuple[bool, valid_types]:
        """
        A function that checks whether an input can be casted to
        the expected type and returns it casted.

        Args:
            given_input_string (str): The input to check.
            expected_type (valid_types): The expected type of the input.

        Returns:
            Tuple[bool, valid_types]: Whether it was a valid input for
                the expected type, and the input as a string or casted
                to the expected type.
        """
        try:
            given_input = expected_type(given_input_string)
        except:
            print(f"Error, type expected: {expected_type}, " +
                  f"given: {given_input_string} " +
                  f"\nTries left: {self._tries_}\n")
            return False, given_input_string
        return True, given_input

    def __check_options_complience(self,
                                   given_input: valid_types,
                                   options: list
                                   ) -> bool:
        """
        Function that checks if the input is of an option from a
        set of options.

        Args:
            given_input (valid_types): The input casted to it's
                expected type.
            options (list): The list of options to be checked against.

        Returns:
            bool: Whether the input is part of the list of options.
        """
        if options != [] and given_input not in options:
            print(f"Error, input not in expected options, "+
                  f"given: {given_input}, expected: {options}\n" +
                  f"Tries left: {self._tries_}\n")
            return False
        return True
