#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of SysPass Client
#
# Copyright (C) 2020  DigDeo SAS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import random
import string
import six
import syspassclient
from colorama import init, Fore, Style
import threading

lock = threading.Lock()
init(autoreset=True)


class Libs(syspassclient.Object, syspassclient.CheckType, syspassclient.Api):
    def __init__(self):
        syspassclient.Object.__init__(self)
        syspassclient.CheckType.__init__(self)
        syspassclient.Api.__init__(self)
        if self.api_data is None:
            self.read_api()
            # API File loading
            # print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format("LIBS"), end='')
            # print(Fore.WHITE + Style.BRIGHT + "{0} v{1}".format("Preload API", self.api_version))
            #
            # print(Fore.WHITE + Style.BRIGHT + "File: ", end='')
            # print(Fore.GREEN + Style.BRIGHT + "{0}".format(self.api_file))

    def look_for_error(self, data, req):
        """
        Raise when a key name 'error' is found.

        The function try to make tests for know if the error message is come back with the a keys': \
        'message', 'code', 'data'

        :param data: a JSon text as originally send to SysPass
        :type: dict
        :param req: a JSon text as return by SysPass
        :type req: dict
        """
        self.is_dict_or_raise(data)
        self.is_dict_or_raise(req)
        if "error" in req:
            error_message = ""
            error_message += "method: "
            error_message += str(data["method"])
            if "message" in req["error"]:
                if req["error"]["message"] == "Internal error":
                    raise ValueError('syspass client have return a Internal error, all operation is stopped')

    def look_for_args(self, **parameters):
        """
        Check Args for a method, it function try to Raise

        Test if the method exit on the API version

        #. Test if it have wrong parameters

        #. Test if every require parameters have been set

        #. Test the type of each parameter

        :param parameters: dict of parameters key=value
        :type parameters: keys
        """
        self.look_for_valid_method(parameters=parameters)
        self.look_for_parameters_injection(parameters=parameters)
        self.look_for_required_params(parameters=parameters)
        self.look_for_parameters_type(parameters=parameters)

    def look_for_parameters_type(self, **parameters):
        if "parameters" in parameters:
            parameters = parameters["parameters"]

        if "method" not in parameters:
            raise (KeyError('"parameters" must have a key name "method"'))

        for parameter, value in parameters.items():
            # Move to next iteration when parameter is 'method'
            if parameter == "method":
                continue

            # Test parameter type:
            # Str type
            if parameters["method"] and \
                    self.api_data[parameters["method"]]["params_details"][parameter]["type"] == "str":

                # If parameter is not require it can be None
                if parameter in self.required_parameters(parameters["method"]):
                    if not isinstance(value, six.string_types):
                        raise TypeError("{0} must be a str instance, here that a {1}".format(parameter, type(value)))
                else:
                    if not isinstance(value, six.string_types) and value is not None:
                        raise TypeError(
                            "{0} must be a str instance or None, here that a {1}".format(parameter, type(value))
                        )

            # Int Type
            elif parameters["method"] and \
                    self.api_data[parameters["method"]]["params_details"][parameter]["type"] == "int":

                # If parameter is not require it can be None
                if parameter in self.required_parameters(parameters["method"]):

                    if type(int()) != type(value):
                        raise TypeError(
                            "{0} must be a int instance, here that a {1}".format(parameter, str(type(value)))
                        )
                else:
                    if type(int()) != type(value) and value is not None:
                        raise TypeError(
                            "{0} must be a int instance or None, here that a {1}".format(parameter, str(type(value)))
                        )
            # List
            elif parameters["method"] and \
                    self.api_data[parameters["method"]]["params_details"][parameter]["type"] == "array":
                # Never a array is in require parameter, and that for API v3.0 and v3.1
                if list != type(value) and value is not None:
                    raise TypeError(
                        "{0} must be a list instance or None, here that a {1}".format(parameter, str(type(value)))
                    )

    def look_for_parameters_injection(self, **parameters):
        """
        Internal function it look if it haven't wrong parameter, only parameters define on the API can be valid.

        :param parameters: a keys name, keys value dictionary
        :type parameters: kwargs
        """
        if "parameters" in parameters:
            parameters = parameters["parameters"]

        if "method" not in parameters:
            raise (KeyError('"parameters" must have a key name "method"'))

        # method = parameters['method']
        # del parameters['method']

        for parameter, value in parameters.items():
            if parameter == "method":
                continue
            if "params_details" in self.api_data[parameters["method"]]:
                if parameter not in self.api_data[parameters["method"]]["params_details"]:
                    raise (
                        AttributeError(
                            '"{0}" is not a valid parameter for syspass api {1}'.format(
                                parameter, syspassclient.dd.syspass["api"]["version"]
                            )
                        )
                    )

    @staticmethod
    def look_for_valid_method(**parameters):
        """
        Internal function it check if a method is valid in the actual API version

        :param parameters: a keys name, keys value dictionary
        :type parameters: kwargs
        """

        if "parameters" in parameters:
            parameters = parameters["parameters"]

        if "method" not in parameters:
            raise (KeyError('"parameters" must have a key name "method"'))

        method = syspassclient.dd.syspass["api"][syspassclient.dd.syspass["api"]["version"]]["methods"]
        if parameters["method"] not in method:
            raise (
                ValueError(
                    "method: {0} is not a valid on version {1} of the syspass api".format(
                        parameters["method"], syspassclient.dd.syspass["api"]["version"]
                    )
                )
            )

    def required_parameters(self, method):
        """
        Return a list of require item, for a special method name

        *example*

        for method='account/create'

        it should return

        ['authToken', 'categoryId', 'clientId', 'name', 'password', 'tokenPass']

        :param method: the name of the method
        :type method: str
        :return: a list of required key
        :rtype: list
        """
        requirement_list = []
        for parameter in self.api_data[method]["params_details"]:
            if self.api_data[method]["params_details"][parameter]["required"] is True:
                requirement_list.append(parameter)
        return requirement_list

    def look_for_required_params(self, **parameters):
        """
        Internal function if look if every parameters is present for a method.
        The parameter args must contain a key name 'method'

        :type parameters: kwargs
        """
        if "parameters" in parameters:
            parameters = parameters["parameters"]

        if "method" not in parameters:
            raise (KeyError('"parameters" must have a key name "method"'))

        for required_parameter in self.required_parameters(parameters["method"]):
            if required_parameter not in parameters:
                raise (
                    AttributeError(
                        'method:{0} is require "{1}" parameter'.format(parameters["method"], required_parameter)
                    )
                )

    def merge_dictionary(self, source=None, target=None):
        """
        Merge two dicts

        :param target:
        :type target: dict
        :param source:
        :type source: dict
        :return: the merged dict
        :rtype: dict
        """
        self.is_dict_or_raise(source)
        self.is_dict_or_raise(target)

        for key, value in source.items():
            if key not in target:
                target[key] = value
            else:
                if target[key] != value:
                    target[key] = value
            # else:
            #     target[key] = merge_dictionary(target[key], value)

        return target

    @staticmethod
    def random_string(choice=string.ascii_lowercase, length=40, prefix=None):
        """
        Generate a random string of fixed length

        :param choice:
        :param length: the length of the returned string
        :type length: int
        :param prefix: use a prefix
        :type prefix: str or None
        :return: a string build with random function
        :rtype: str
        """
        if prefix is None:
            prefix = ""
        if type(prefix) != str:
            raise TypeError("'prefix' parameter must be a str type")

        return "{0}{1}".format(
            prefix,
            "".join(random.choice(choice) for _ in range(length))
        )
