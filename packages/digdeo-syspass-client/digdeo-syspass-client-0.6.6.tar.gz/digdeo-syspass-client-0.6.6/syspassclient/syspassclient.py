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

import syspassclient
import codecs
import os.path

from colorama import init, Fore, Style

init(autoreset=True)

import requests

from json.decoder import JSONDecodeError

from yaml import dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class SyspassClient(syspassclient.Config):
    def __init__(
            self,
            use_by_lookup=None,
            api_url=None,
            api_version=None,
            authToken=None,
            tokenPass=None,
            verify_ssl=None,
            debug=None,
            debug_level=None,
            verbose=None,
            verbose_level=None,
    ):

        # Private property's
        self.__r_id = None

        # Initialize
        if debug:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "{0}: ".format(self.__class__.__name__.upper()),
                end="",
            )
            print(Fore.WHITE + Style.NORMAL + "version ", end="")
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(syspassclient.__version__))

        self.r_id = 1

        syspassclient.Config.__init__(self)
        # Look init var have been set
        if use_by_lookup:  # pragma: no cover
            self.use_by_lookup = use_by_lookup
        if api_url:
            self.api_url = api_url
        if api_version:
            self.api_version = api_version
        if authToken:
            self.authToken = authToken
        if tokenPass:
            self.tokenPass = tokenPass
        if verify_ssl:
            self.verify_ssl = verify_ssl
        if debug:
            self.debug = debug
        if debug_level:
            self.debug_level = debug_level
        if verbose:
            self.verbose = verbose
        if verbose_level:
            self.verbose_level = verbose_level

        if not self.use_by_lookup:
            self.config_read_file()

        if self.debug:
            self.display_resume()

    def make_post_request(self, data=None, verify=None):
        """
        Make the request ith the 'requests' python module.

        :param data: the data it will be convert on json
        :type data: dict or str
        :param verify: SSL certificate verification
        :type verify: bool
        :return: the request.post return
        :rtype: dict
        """
        if verify is None:
            verify = self.verify_ssl

        if self.verbose:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "{0}: ".format(self.__class__.__name__.upper()),
                end="",
            )
            print(Fore.WHITE + Style.BRIGHT + "{0} ".format(data["method"]))
            for line in dump(data).split("\n"):
                if line is not None and line != "":
                    print(
                        Fore.GREEN
                        + Style.BRIGHT
                        + "> "
                        + Fore.RESET
                        + Style.RESET_ALL
                        + str(line)
                    )
            print(Fore.RESET + Style.RESET_ALL, end="")

        request = requests.post(url=self.api_url, json=data, verify=verify)

        try:
            return request.json()
        except JSONDecodeError:  # pragma: no cover
            # In case we don't receive json thing
            return request.text

    def increase_request_id(self, increment=1):
        """
        In case of multi request, request ID must be increase for permit to the API work with.

        :param increment: a increment value
        :type increment: int
        :raise TypeError: if ``increment`` is not a int
        :raise ValueError: if ``increment`` is not a positive value
        """
        self.is_int_or_raise(increment)

        if increment <= 0:
            raise ValueError("'increment' must be a positive value")

        self.r_id += increment

    def generate_json(self, **parameters):
        """
        Internal function it generate a valid request in JSON format

        That function clean the request and mitigate python reserved name, like **Global**, **Id**, **Pass**

        For parameter's list take a look on SysPass API:
        * https://syspass-doc.readthedocs.io/en/3.0/application/api.html
        * https://syspass-doc.readthedocs.io/en/3.1/application/api.html

        :param parameters: The parameters pass to syspass API
        :type parameters: keys
        :return: The parameters format in valid JSON 2.0
        :rtype: str
        :raise KeyError: When parameters don't contain a key name "method"
        """

        # if "method" not in parameters:
        #     raise (KeyError('"parameters" must have a key name "method"'))
        method = parameters["method"]
        del parameters["method"]

        # workaround about 'pass' python world reserved
        if "password" in parameters:
            password = parameters["password"]
            del parameters["password"]
            parameters["pass"] = password

        # workaround for 'global' world reserved
        if "Global" in parameters:
            Global = parameters["Global"]
            del parameters["Global"]
            parameters["global"] = Global

        # workaround for 'id' world reserved
        if "ugid" in parameters:
            ugid = parameters["ugid"]
            del parameters["ugid"]
            parameters["id"] = ugid

        if "cid" in parameters:
            cid = parameters["cid"]
            del parameters["cid"]
            parameters["id"] = cid

        if "tagid" in parameters:
            tagid = parameters["tagid"]
            del parameters["tagid"]
            parameters["id"] = tagid

        if "account_id" in parameters:
            account_id = parameters["account_id"]
            del parameters["account_id"]
            parameters["id"] = account_id

        # Small clean up
        for key, value in dict(parameters).items():
            if value is None:  # pragma: no cover
                del parameters[key]
            if value is []:  # pragma: no cover
                del parameters[key]

        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": parameters,
            "id": self.r_id,
        }

    def print_returned_value(self, req):
        """
        Internal function to print returned value.

        Printed values depends of ``verbose`` and ``verbose_level`` properties

        :param req: The return of requests module as a dict
        :type req: dict
        """
        if self.verbose:
            if self.verbose_level > 1:
                print(
                    Fore.YELLOW
                    + Style.BRIGHT
                    + "{0}: ".format(self.__class__.__name__.upper()),
                    end="",
                )
                print(Fore.WHITE + Style.BRIGHT + "Returned Value")

            if "error" in req:
                for line in dump(req, allow_unicode=True).split("\n"):
                    if line is not None and line != "":
                        print(
                            Fore.CYAN
                            + Style.BRIGHT
                            + "< "
                            + Fore.RED
                            + Style.BRIGHT
                            + str(line)
                        )
            else:
                for line in dump(req, allow_unicode=True).split("\n"):
                    if line is not None and line != "":
                        print(
                            Fore.CYAN
                            + Style.BRIGHT
                            + "< "
                            + Fore.RESET
                            + Style.RESET_ALL
                            + str(line)
                        )
            print(Fore.RESET + Style.RESET_ALL, end="")

    def account_search(
            self,
            method="account/search",
            authToken=None,
            text=None,
            count=None,
            categoryId=None,
            clientId=None,
            tagsId=None,
            op=None,
            matchall=None,
    ):
        """
        Search for accounts

        parameter ``match_all`` is not on the original API

        :param method: the method name
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param text: Text to search for
        :type text: str or None
        :param count: Number of results to display
        :type count: int or None
        :param categoryId: Category’s Id for filtering
        :type categoryId: int or None
        :param clientId: Client’s Id for filtering
        :type clientId: int or None
        :param tagsId: Tags’ Id for filtering
        :type tagsId: array or None
        :param op: Operator used for filtering. It can be either ‘or’ or ‘and’
        :type: op: str or None
        :param matchall:
        :type matchall:
        :return: Return the searching result str in case of success or None if nothing found
        :rtype: str or None
        """
        if authToken is None:
            authToken = self.authToken

        # Exit as soon of possible
        self.look_for_args(
            method=method,
            authToken=authToken,
            text=text,
            count=count,
            categoryId=categoryId,
            clientId=clientId,
            tagsId=tagsId,
            op=op,
        )

        data = self.generate_json(
            method=method,
            authToken=authToken,
            text=text,
            count=count,
            categoryId=categoryId,
            clientId=clientId,
            tagsId=tagsId,
            op=op,
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)
        return self.controlled_match_all(req=req, matchall=matchall, text=text)

    @staticmethod
    def controlled_match_all(req=None, matchall=None, text=None):
        """
        Internal function it control match_all mechanic

        :param req: The requests python module return
        :type req: dict
        :param matchall: If True the returned value contain all it match with the request
        :param text:
        :return:
        """
        if matchall is None:
            matchall = False

        if type(matchall) != bool:
            raise TypeError("'matchall' must be a bool type or None")

        if type(req) != dict:
            raise TypeError("'req' must be a dict type")

        if (
                "result" in req
                and "count" in req["result"]
                and req["result"]["count"] > 0
                and "result" in req["result"]
        ):
            if matchall is False:
                for res in req["result"]["result"]:
                    if res["name"].upper() == text.upper():
                        return res["id"]
            else:
                if "id" in req["result"]["result"][0]:
                    return req["result"]["result"][0]["id"]
        else:
            return None

    def account_delete(self, method="account/delete", authToken=None, account_id=None):
        """
        Delete an account

        :param method: must be ``account/delete``
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param account_id: Account’s Id
        :type account_id: int
        """
        if authToken is None:
            authToken = self.authToken

        # Exit as soon of possible
        self.look_for_args(method=method, authToken=authToken, account_id=account_id)

        data = self.generate_json(
            method=method, authToken=authToken, account_id=account_id
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if req["result"]["resultCode"] == 0:
            return req["result"]
        # else:
        #     raise AnsibleError("AccountDelete Error : %s" % req)

    def account_view(
            self, method="account/view", authToken=None, tokenPass=None, account_id=None
    ):
        """
        Search for accounts:

        :param method: the method name
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param tokenPass: API token’s pass, is used to decrypt encrypted data.
        :type tokenPass: str
        :param account_id:  Account’s Id
        :type account_id: int
        """
        if authToken is None:
            authToken = self.authToken

        if tokenPass is None:
            tokenPass = self.tokenPass

        self.look_for_args(
            method=method,
            authToken=authToken,
            tokenPass=tokenPass,
            account_id=account_id,
        )

        data = self.generate_json(
            method=method,
            authToken=authToken,
            tokenPass=tokenPass,
            account_id=account_id,
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if (
                "result" in req
                and "result" in req["result"]
                and len(req["result"]["result"]) > 0
        ):
            return req["result"]["result"]
        else:  # pragma: no cover
            return None

    def account_viewpass(
            self,
            method="account/viewPass",
            authToken=None,
            tokenPass=None,
            account_id=None,
            details=None,
    ):
        """
        Get account’s password

        :param method: the method name
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param tokenPass: API token’s pass, is used to decrypt encrypted data.
        :type tokenPass: str
        :param account_id: Account’s Id
        :type account_id: int
        :param details: Whether to return account’s details within response
        :type details: int or None
        """
        if authToken is None:
            authToken = self.authToken

        if tokenPass is None:
            tokenPass = self.tokenPass

        self.look_for_args(
            method=method,
            authToken=authToken,
            tokenPass=tokenPass,
            account_id=account_id,
            details=details,
        )

        data = self.generate_json(
            method=method,
            authToken=authToken,
            tokenPass=tokenPass,
            account_id=account_id,
            details=details,
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        # We got a response
        if "result" in req and "count" in req["result"] and req["result"]["count"] > 0:
            return req["result"]["result"]["password"]
        # else:
        #     raise AnsibleError('AccountViewpass Error : %s' % req)

    def account_create(
            self,
            method="account/create",
            authToken=None,
            tokenPass=None,
            name=None,
            categoryId=None,
            clientId=None,
            password=None,
            tagsId=None,
            userGroupId=None,
            parentId=None,
            login=None,
            url=None,
            notes=None,
            private=None,
            privateGroup=None,
            expireDate=None,
    ):
        """
        Create account

        Note: pass have been change by password, due that a python reserved world. That is the json request creator it
        change password for pass just at end of the process.

        :param method: must be ``account/create``.
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param tokenPass: API token’s pass
        :type tokenPass: str
        :param name: Account’s name
        :type name: str
        :param categoryId: Account’s category Id
        :type categoryId: int
        :param clientId: Account’s client Id
        :type clientId: int
        :param password: Account’s password
        :type password: str
        :param tagsId: Account’s tags Id
        :type tagsId: list
        :param userGroupId: Account’s user group Id
        :type userGroupId: int
        :param parentId: Account’s parent Id
        :type parentId: int or None
        :param login: Account’s login
        :type login: str
        :param url: Account’s access URL or IP
        :type url: str
        :param notes: Account’s notes
        :type notes: str
        :param private: Set account as private. It can be either 0 or 1
        :type private: int
        :param privateGroup: Set account as private for group. It can be either 0 or 1
        :type privateGroup: int
        :param expireDate: Expire date in UNIX timestamp format
        :type expireDate: int
        """
        if authToken is None:
            authToken = self.authToken

        if tokenPass is None:
            tokenPass = self.tokenPass

        if expireDate == "":  # pragma: no cover
            expireDate = None

        self.look_for_args(
            method=method,
            authToken=authToken,
            tokenPass=tokenPass,
            name=name,
            categoryId=categoryId,
            clientId=clientId,
            password=password,
            tagsId=tagsId,
            userGroupId=userGroupId,
            parentId=parentId,
            login=login,
            url=url,
            notes=notes,
            private=private,
            privateGroup=privateGroup,
            expireDate=expireDate,
        )

        data = self.generate_json(
            method=method,
            authToken=authToken,
            tokenPass=tokenPass,
            name=name,
            categoryId=categoryId,
            clientId=clientId,
            password=password,
            tagsId=tagsId,
            userGroupId=userGroupId,
            parentId=parentId,
            login=login,
            url=url,
            notes=notes,
            private=private,
            privateGroup=privateGroup,
            expireDate=expireDate,
        )
        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if req["result"]["itemId"] > 0:
            return req["result"]["itemId"]
        else:  # pragma: no cover
            return None

    def category_search(
            self, method="category/search", authToken=None, text=None, count=1000
    ):
        """
        Searches syspass category.

        :param method: must be category/search
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param text: text is the keyword.
        :type text: str
        :param count: the number of results.
        :type count: int
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, text=text, count=count)

        data = self.generate_json(
            method=method, authToken=authToken, text=text, count=count
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)

        # We got a response

        # print('################################################')
        # for res in req['result']['result']:
        #     print(dump(res))
        # print('################################################')

        if (
                "result" in req
                and "count" in req["result"]
                and req["result"]["count"] > 0
                and "result" in req["result"]
        ):
            for res in req["result"]["result"]:
                if res["name"].upper() == text.upper():
                    return res["id"]
        else:  # pragma: no cover
            return None

    def category_create(
            self, method="category/create", authToken=None, name=None, description=None
    ):
        """
        Create category

        :param method: must be category/create
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param name: Category’s name
        :type name: str
        :param description: Category’s description
        :type description: str
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(
            method=method, authToken=authToken, name=name, description=description
        )

        data = self.generate_json(
            method=method, authToken=authToken, name=name, description=description
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)
        if (
                "result" in req
                and "itemId" in req["result"]
                and req["result"]["itemId"] > 0
                and req["result"]["itemId"] is not None
        ):
            return req["result"]["itemId"]
        else:  # pragma: no cover
            return self.category_search(text=name)

    def category_delete(self, method="category/delete", authToken=None, cid=None):
        """
        Delete category

        :param method: must be category/delete
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param cid: Category’s Id
        :type cid: int
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, cid=cid)

        data = self.generate_json(method=method, authToken=authToken, cid=cid)

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if req["result"]["resultCode"] == 0:
            return req["result"]
        # else:
        #     raise AnsibleError("CategoryDelete Error : %s" % req)

    def client_search(
            self, method="client/search", authToken=None, text=None, count=None
    ):
        """
        Search for clients

        :param method: must be ``client/search``
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param text: Text to search for
        :type text: str
        :param count: Number of results to display
        :type count: int
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, text=text, count=count)

        data = self.generate_json(
            method=method, authToken=authToken, text=text, count=count
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)

        # We got a response
        if (
                "result" in req
                and "count" in req["result"]
                and req["result"]["count"] > 0
                and "result" in req["result"]
        ):
            for res in req["result"]["result"]:
                if res["name"].upper() == text.upper():
                    return res["id"]
        else:  # pragma: no cover
            return None

    def client_create(
            self,
            method="client/create",
            authToken=None,
            name=None,
            description=None,
            Global=False,
    ):
        """
        Creates a syspass client.

        :param method: must be 'client/create'
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param name: Client’s name
        :type name: str
        :param description: Client’s description
        :type description: str
        :param Global: Set client as global. It can be either 0 or 1
        :type Global: int
        """
        if authToken is None:
            authToken = self.authToken

        if Global is not None:
            Global = int(bool(Global))

        self.look_for_args(
            method=method,
            authToken=authToken,
            name=name,
            description=description,
            Global=Global,
        )

        data = self.generate_json(
            method=method,
            authToken=authToken,
            name=name,
            description=description,
            Global=Global,
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)

        if (
                "result" in req
                and "itemId" in req["result"]
                and req["result"]["itemId"] > 0
        ):
            return req["result"]["itemId"]

        return self.client_search(text=name)

    def client_delete(self, method="client/delete", authToken=None, cid=None):
        """
        Delete client

        :param method: must be 'client/create'
        :type method: str
        :param authToken: User’s API token
        :type: authToken: str
        :param cid: Client’s Id
        :type cid: int
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, cid=cid)

        data = self.generate_json(method=method, authToken=authToken, cid=cid)

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if (
                "result" in req
                and "resultCode" in req["result"]
                and req["result"]["resultCode"] == 0
        ):
            return req["result"]["resultCode"]
        else:
            return None

    def tag_search(self, method="tag/search", authToken=None, text=None):
        """
        Search for tags

        :param method: must be "tag/search"
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param text: Tag’s name
        :type text: str
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, text=text)

        data = self.generate_json(method=method, authToken=authToken, text=text)

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)

        if (
                "result" in req
                and "result" in req["result"]
                and len(req["result"]["result"]) > 0
        ):
            for reponse in req["result"]["result"]:
                if "name" in reponse and reponse["name"] == text:
                    return reponse["id"]

        return None

    def tag_view(self, method="tag/view", authToken=None, tokenPass=None, tagid=None):
        """
        Search for tags

        :param method: must be "tag/search"
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param tokenPass: Text to search for
        :type tokenPass: str
        :param tagid: Tag’s Id
        :type tagid: int
        """
        if authToken is None:
            authToken = self.authToken

        if tokenPass is None:
            tokenPass = self.tokenPass

        self.look_for_args(
            method=method, authToken=authToken, tokenPass=tokenPass, tagid=tagid
        )

        data = self.generate_json(
            method=method, authToken=authToken, tokenPass=tokenPass, tagid=tagid
        )

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if (
                "result" in req
                and "result" in req["result"]
                and len(req["result"]["result"]) > 0
                and "name" in req["result"]["result"]
        ):
            return req["result"]["result"]["name"]
        else:  # pragma: no cover
            return None

    def tag_create(self, method="tag/create", authToken=None, name=None):
        """
        Create tag

        :param method: must be "tag/search"
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param name: Tag’s name
        :type name: str
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, name=name)

        data = self.generate_json(method=method, authToken=authToken, name=name)

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        # look_for_error(data, req)

        if (
                "result" in req
                and "itemId" in req["result"]
                and req["result"]["itemId"] > 0
        ):
            return req["result"]["itemId"]

        return self.tag_search(text=name)

    def tag_delete(self, method="tag/delete", authToken=None, tagid=None):
        """
        Delete a tag

        :param method: must be 'tag/delete'
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param tagid: Tag’s Id
        :type tagid: int
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, tagid=tagid)

        data = self.generate_json(method=method, authToken=authToken, tagid=tagid)

        self.increase_request_id()

        req = self.make_post_request(data)

        self.print_returned_value(req)

        self.look_for_error(data, req)

        if "result" in req and "resultCode" in req["result"]:
            return req["result"]["resultCode"]
        else:  # pragma: no cover
            return None
        # if req['result']['resultCode'] == 0:
        #     return req['result']
        # else:
        #     raise AnsibleError('TagDelete Error : %s' % (req))

    def user_group_create(
            self,
            method="userGroup/create",
            authToken=None,
            name=None,
            description=None,
            usersId=None,
    ):
        """
        userGroup/create

        :param method: must be 'userGroup/create'
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param name: User group’s name
        :type name: str
        :param description: User group’s description
        :type description: str
        :param usersId: User group’s users Id
        :type usersId: list
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(
            method=method,
            authToken=authToken,
            name=name,
            description=description,
            usersId=usersId,
        )
        data = self.generate_json(
            method=method,
            authToken=authToken,
            name=name,
            description=description,
            usersId=usersId,
        )
        self.increase_request_id()
        req = self.make_post_request(data)
        self.print_returned_value(req)

        # look_for_error(data, req)
        if (
                "result" in req
                and "itemId" in req["result"]
                and req["result"]["itemId"] > 0
        ):
            return req["result"]["itemId"]

        return self.user_group_search(text=name)

    def user_group_search(
            self, method="userGroup/search", authToken=None, text=None, count=None
    ):
        """
        Search for user groups

        :param method: must be ``userGroup/search``
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param text: Text to search for
        :type text: str
        :param count: Number of results to display
        :type count: int
        """

        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, text=text, count=count)
        data = self.generate_json(
            method=method, authToken=authToken, text=text, count=count
        )
        self.increase_request_id()
        req = self.make_post_request(data)
        self.print_returned_value(req)

        if (
                "result" in req
                and "count" in req["result"]
                and req["result"]["count"] > 0
                and "result" in req["result"]
        ):
            for res in req["result"]["result"]:
                if res["name"].upper() == text.upper():
                    return res["id"]

        else:  # pragma: no cover
            self.look_for_error(data, req)
            return None

    # SYSPASSCLIENT: userGroup/search
    # > id: 27
    # > jsonrpc: '2.0'
    # > method: userGroup/search
    # > params:
    # >   authToken: b865b432f553960c1b1a8742a21f54885401b9abb37649d81d0d065f37183eb4
    # >   text: FOR_TEST
    # syspass_api_url: https://prepsyspass.ddprep.digdeo.net/api.php
    # < id: 27
    # < jsonrpc: '2.0'
    # < result:
    # <   count: 1
    # <   itemId: 0
    # <   result:
    # <   - description: a UserGroup for test
    # <     id: 1412
    # <     name: FOR_TEST
    # <     users: null
    # <   resultCode: 0
    # <   resultMessage: null
    def user_group_delete(self, method="userGroup/delete", authToken=None, ugid=None):
        """
        Delete user group

        :param method: must be ``userGroup/delete``
        :type method: str
        :param authToken: User’s API token
        :type authToken: str
        :param ugid: User group’s Id
        :type ugid: int
        """
        if authToken is None:
            authToken = self.authToken

        self.look_for_args(method=method, authToken=authToken, ugid=ugid)
        data = self.generate_json(method=method, authToken=authToken, ugid=ugid)
        self.increase_request_id()
        req = self.make_post_request(data)
        self.print_returned_value(req)

        if (
                "result" in req
                and "resultCode" in req["result"]
                and req["result"]["resultCode"] == 0
        ):
            return req["result"]
        else:  # pragma: no cover
            return None
            # look_for_error(data, req)

#
#     def Backup(self):
#         """
#         https://github.com/nuxsmin/sysPass/issues/1004#issuecomment-411487284
#         """
#         data = {"jsonrpc": "2.0",
#                 "method": "backup",
#                 "params": {
#                     "authToken": self.api_key,
#                 },
#                 "id": self.r_id
#                 }
#
#         self.r_id += 1
#         req = requests.post(self.api_url, json=data, verify=False)
#         if 'result' in req.json():
#             return req.json()['result']
#         else:
#             raise AnsibleError('Backup Error : %s' % (req.json()))
#
#
