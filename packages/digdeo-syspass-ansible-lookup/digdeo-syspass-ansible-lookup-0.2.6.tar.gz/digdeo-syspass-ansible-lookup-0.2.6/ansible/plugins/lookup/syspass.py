#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of Ansible Lookup SysPass
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

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# Make coding more python3-ish, this is required for contributions to Ansible

from __future__ import absolute_import, division, print_function
from ansible.parsing.yaml.objects import AnsibleUnicode
from ansible.utils.unsafe_proxy import AnsibleUnsafeText
from colorama import init, Fore, Style

init(autoreset=True)
__metaclass__ = type
__version__ = "0.2.6"

DOCUMENTATION = """
        DISCLAIMER: This module has been heavily inspired by https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/lookup/password.py for password generation and term handling and thus is under GPL.
        
        lookup: syspass
        author: Gousseaud Gaëtan <gousseaud.gaetan.pro@gmail.com>, Pierre-Henry Muller <pierre-henry.muller@digdeo.fr>, Tuxa <tuxa@rtnp.org>
        short_description: get syspass user password and syspass API client
        description:
            - This lookup returns the contents from Syspass database, a user's password more specifically. Other functions are also implemented for further use.
        ansible_version: ansible 2.7.17 with mitogen
        python_version: 3.7
        syspass_version: 3.1
        params:
            -term: the account name (required and must be unique)
            -login: login given to created account
            -category: category given to created account
            -customer: client given to created account
            -state: like in Ansible absent to remove the password, present in default to create (Optional)
            -pass_length: generated password length (Optional)
            -chars: type of chars used in generated (Optional)
            -url: url given to created account (Optional)
            -notes: notes given to created account (Optional)
            -private: is this password private for users who have access or public for all users in acl (default false)
            -privategroup: is private only for users in same group (default false)
            -expirationDate: expiration date given to created account (Optional) and not tested (no entry in webui)
        notes:
            - Account is only created if exact name has no match.
            - A different field passed to an already existing account wont modify it.
            - Utility of tokenPass: https://github.com/nuxsmin/sysPass/issues/994#issuecomment-409050974
            - Rudimentary list of API accesses (Deprecated): https://github.com/nuxsmin/sysPass/blob/d0056d74a8a2845fb3841b02f4af5eac3e4975ed/lib/SP/Services/Api/ApiService.php#L175
            - Usage of ansible vars: https://github.com/ansible/ansible/issues/33738#issuecomment-350819222
        syspass function list:
            SyspassClient:
                Account:
                    -AccountSearch
                    -AccountViewpass
                    -AccountCreate
                    -AccountDelete
                    -AccountView
                Category:
                    -CategorySearch
                    -CategoryCreate
                    -CategoryDelete
                Client:
                    -ClientSearch
                    -ClientCreate
                    -ClientDelete
                Tag:
                    -TagCreate
                    -TagSearch
                    -TagDelete
                UserGroup:
                    - UserGroupCreate
                    - UserGroupSearch
                    - UserGroupDelete
                Others:
                    -Backup
"""
EXAMPLES = """
### IN HOST VARS ###

syspass_API_URL: http://syspass-server.net/api.php
syspass_API_KEY: 'API_KEY' #Found in Users & Accesses -> API AUTHORIZATION -> User token
syspass_API_ACC_TOKPWD: Password for API_KEY for Account create / view / delete password account permission in API
syspass_default_length: number of chars in password

### IN PLAYBOOK ###

NOTE: Default values are handled 

##### USAGE 1 #####

- name: Minimum declaration to get / create password
  local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', login=test, category='MySQL', customer='Customer 1') }}"

- name: All details for password declaration
  local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', login=test, category='MySQL', customer='Customer 1', 
    url='https://exemp.le', notes='Additional information', private=True, privategroupe=True) }}"

- name: Minimum declaration to delete password
  local_action: debug msg="{{ lookup('syspass', 'Server 1 test account', state=absent) }}"


"""
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

# from ansible.module_utils._text import to_native, to_text

display = Display()

import random
import warnings
from urllib3.exceptions import HTTPWarning, InsecureRequestWarning

warnings.simplefilter("ignore", HTTPWarning)
warnings.simplefilter("ignore", InsecureRequestWarning)

import syspassclient


class LookupModule(LookupBase):
    def __init__(self, loader=None, templar=None, **kwargs):
        LookupBase.__init__(self, loader=loader, templar=templar, kwargs=kwargs)
        # Private property's

        self.__verbose = None
        self.__verbose_level = None
        self.__debug = None
        self.__debug_level = None
        self.debug = True
        self.debug_level = 3
        self.verbose = True
        self.verbose_level = 3

        self.__syspass_client = None
        self.__term = None
        self.__variables = None
        self.__kwargs = None
        self.__params = None
        # Property Mess
        self.__account = None
        self.__chars = None
        self.__syspass_API_URL = None
        self.__syspass_API_KEY = None
        self.__syspass_API_ACC_TOKPWD = None
        self.__syspass_default_length = None
        # Default DigDeo Client vars
        self.__DD_SYSPASS_CLIENT_CONFIG_DIR = None
        self.__DD_SYSPASS_CLIENT_AUTH_TOKEN = None
        self.__DD_SYSPASS_CLIENT_TOKEN_PASS = None
        self.__DD_SYSPASS_CLIENT_VERIFY_SSL = None
        self.__DD_SYSPASS_CLIENT_API_URL = None
        self.__DD_SYSPASS_CLIENT_API_VERSION = None
        self.__DD_SYSPASS_CLIENT_DEBUG = None
        self.__DD_SYSPASS_CLIENT_DEBUG_LEVEL = None
        self.__DD_SYSPASS_CLIENT_VERBOSE = None
        self.__DD_SYSPASS_CLIENT_VERBOSE_LEVEL = None
        self.__password_length = None
        self.__password_length_min = 8
        self.__password_length_max = 100
        self.__password = None
        self.__hostname = None
        self.__login = None
        self.__category = None
        self.__customer = None
        self.__customer_desc = None
        self.__tags = None
        self.__url = None
        self.__notes = None
        self.__state = None
        self.__private = None
        self.__privategroup = None
        self.__expireDate = None

        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "{0}: ".format(self.__class__.__name__.upper()),
            end="",
        )
        print(Fore.WHITE + Style.NORMAL + "version ", end="")
        print(Fore.GREEN + Style.BRIGHT + "{0}".format(__version__))

        # First init
        self.params = None
        # self.term = None
        self.syspass_client = syspassclient.SyspassClient(use_by_lookup=True)

        # Default DigDeo Client vars
        self.DD_SYSPASS_CLIENT_CONFIG_DIR = None
        self.DD_SYSPASS_CLIENT_AUTH_TOKEN = None
        self.DD_SYSPASS_CLIENT_TOKEN_PASS = None
        self.DD_SYSPASS_CLIENT_VERIFY_SSL = None
        self.DD_SYSPASS_CLIENT_API_URL = None
        self.DD_SYSPASS_CLIENT_API_VERSION = None
        self.DD_SYSPASS_CLIENT_DEBUG = None
        self.DD_SYSPASS_CLIENT_DEBUG_LEVEL = None
        self.DD_SYSPASS_CLIENT_VERBOSE = None
        self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL = None

        self.syspass_default_length = 40
        self.password_length = self.syspass_default_length
        self.chars = self._gen_candidate_chars(
            ["ascii_letters", "digits", "allowed_punctuation"]
        )
        # self.gen_password()
        # self.password = None
        # self.account = None
        self.hostname = None
        self.login = None
        self.category = None
        self.customer = None
        self.customer_desc = None
        self.tags = None
        self.url = None
        self.notes = None
        self.state = None
        self.private = 0
        self.privategroup = None
        self.expireDate = None

    @property
    def verbose(self):
        """
        Get if the verbose information's is display to the screen.

        :return: True if verbose mode is enable, False for disable it.
        :rtype: bool
        """
        return bool(self.__verbose)

    @verbose.setter
    def verbose(self, verbose):
        """
        Set if the verbose information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param verbose: True is verbose mode is enable, False for disable it.
        :type verbose: bool
        :raise TypeError: when "verbose" argument is not a :py:data:`bool`
        """
        # Exit as soon of possible
        if type(verbose) != bool:
            raise TypeError("'verbose' must be a bool type")

        # make the job in case
        if self.verbose != bool(verbose):
            self.__verbose = bool(verbose)

    @property
    def verbose_level(self):
        """
        Get the verbose information's level to display on the screen.

        Range: 0 to 3

        See: Object.set_verbose_level() for more information's about effect of ``debug_level``

        :return: The debug level as set with MorseDecoder.set_debug_level()
        :rtype: int
        """
        return self.__verbose_level

    @verbose_level.setter
    def verbose_level(self, verbose_level):
        """
        Set the verbose level of information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param verbose_level: The Debug level to set
        :type verbose_level: int
        :raise TypeError: when "verbose_level" argument is not a :py:data:`int`
        """
        # Exit as soon of possible
        if type(verbose_level) != int:
            raise TypeError("'verbose_level' must be a int type")

        # make the job in case
        if self.verbose_level != verbose_level:
            self.__verbose_level = verbose_level

    @property
    def debug(self):
        """
        Get the debugging information's level to display on the screen.

        :return: True if debugging mode is enable, False for disable it.
        :rtype: bool
        """
        return bool(self.__debug)

    @debug.setter
    def debug(self, debug):
        """
        Set the debugging level of information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug: True is debugging mode is enable, False for disable it.
        :type debug: bool
        :raise TypeError: when "debug" argument is not a :py:data:`bool`
        """
        # Exit as soon of possible
        if type(debug) != bool:
            raise TypeError("'debug' must be a bool type")

        # make the job in case
        if self.debug != bool(debug):
            self.__debug = bool(debug)

    @property
    def debug_level(self):
        """
        Get the debugging information's level to display on the screen.

        Range: 0 to 3

        See: MorseDecoder.set_debug_level() for more information's about effect of ``debug_level``

        :return: The debug level as set with MorseDecoder.set_debug_level()
        :rtype: int
        """
        return self.__debug_level

    @debug_level.setter
    def debug_level(self, debug_level):
        """
        Set the debugging level of information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug_level: The Debug level to set
        :type debug_level: int
        :raise TypeError: when "debug_level" argument is not a :py:data:`int`
        """
        # Exit as soon of possible
        if type(debug_level) != int:
            raise TypeError("'debug_level' must be a int type")

        # make the job in case
        if self.debug_level != debug_level:
            self.__debug_level = debug_level

    @property
    def syspass_client(self):
        """
        Property it store the internal syspassClient object

        That is the only one point where store a syspass instance.
        That property flush a first init of SyspassLookup, and can be reset via it property.

        :return: a SyspassClient object instance
        :rtype: SyspassClient
        """
        return self.__syspass_client

    @syspass_client.setter
    def syspass_client(self, syspass_client=None):
        """
        Set the syspass_client property.

        :param syspass_client: a SyspassClient object instance
        :type syspass_client: SyspassClient
        :raise TypeError: when syspass_client is not a SyspassClient object instance
        """
        if not isinstance(syspass_client, syspassclient.SyspassClient):
            raise TypeError(
                "'syspass_client' parameter, must be a SyspassClient instance object"
            )

        if self.syspass_client != syspass_client:
            self.__syspass_client = syspass_client

    @property
    def DD_SYSPASS_CLIENT_AUTH_TOKEN(self):
        return self.__DD_SYSPASS_CLIENT_AUTH_TOKEN

    @DD_SYSPASS_CLIENT_AUTH_TOKEN.setter
    def DD_SYSPASS_CLIENT_AUTH_TOKEN(self, DD_SYSPASS_CLIENT_AUTH_TOKEN=None):
        if (
            DD_SYSPASS_CLIENT_AUTH_TOKEN is not None
            and type(DD_SYSPASS_CLIENT_AUTH_TOKEN) != str
            and type(DD_SYSPASS_CLIENT_AUTH_TOKEN) != AnsibleUnicode
            and type(DD_SYSPASS_CLIENT_AUTH_TOKEN) != AnsibleUnsafeText
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_AUTH_TOKEN' parameter, must be a str type or None"
            )

        if self.DD_SYSPASS_CLIENT_AUTH_TOKEN != DD_SYSPASS_CLIENT_AUTH_TOKEN:
            self.__DD_SYSPASS_CLIENT_AUTH_TOKEN = DD_SYSPASS_CLIENT_AUTH_TOKEN

    @property
    def DD_SYSPASS_CLIENT_TOKEN_PASS(self):
        return self.__DD_SYSPASS_CLIENT_TOKEN_PASS

    @DD_SYSPASS_CLIENT_TOKEN_PASS.setter
    def DD_SYSPASS_CLIENT_TOKEN_PASS(self, DD_SYSPASS_CLIENT_TOKEN_PASS=None):
        if (
            DD_SYSPASS_CLIENT_TOKEN_PASS is not None
            and type(DD_SYSPASS_CLIENT_TOKEN_PASS) != str
            and type(DD_SYSPASS_CLIENT_TOKEN_PASS) != AnsibleUnicode
            and type(DD_SYSPASS_CLIENT_TOKEN_PASS) != AnsibleUnsafeText
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_TOKEN_PASS' parameter, must be a str type or None"
            )

        if self.DD_SYSPASS_CLIENT_TOKEN_PASS != DD_SYSPASS_CLIENT_TOKEN_PASS:
            self.__DD_SYSPASS_CLIENT_TOKEN_PASS = DD_SYSPASS_CLIENT_TOKEN_PASS

    @property
    def DD_SYSPASS_CLIENT_VERIFY_SSL(self):
        return self.__DD_SYSPASS_CLIENT_VERIFY_SSL

    @DD_SYSPASS_CLIENT_VERIFY_SSL.setter
    def DD_SYSPASS_CLIENT_VERIFY_SSL(self, DD_SYSPASS_CLIENT_VERIFY_SSL=None):
        if DD_SYSPASS_CLIENT_VERIFY_SSL is None:
            DD_SYSPASS_CLIENT_VERIFY_SSL = False

        if (
            DD_SYSPASS_CLIENT_VERIFY_SSL is not None
            and type(DD_SYSPASS_CLIENT_VERIFY_SSL) != bool
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_VERIFY_SSL' parameter, must be a bool type or None"
            )

        if self.DD_SYSPASS_CLIENT_VERIFY_SSL != DD_SYSPASS_CLIENT_VERIFY_SSL:
            self.__DD_SYSPASS_CLIENT_VERIFY_SSL = DD_SYSPASS_CLIENT_VERIFY_SSL

    @property
    def DD_SYSPASS_CLIENT_API_URL(self):
        return self.__DD_SYSPASS_CLIENT_API_URL

    @DD_SYSPASS_CLIENT_API_URL.setter
    def DD_SYSPASS_CLIENT_API_URL(self, DD_SYSPASS_CLIENT_API_URL=None):
        if (
            DD_SYSPASS_CLIENT_API_URL is not None
            and type(DD_SYSPASS_CLIENT_API_URL) != str
            and type(DD_SYSPASS_CLIENT_API_URL) != AnsibleUnicode
            and type(DD_SYSPASS_CLIENT_API_URL) != AnsibleUnsafeText
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_API_URL' parameter, must be a str type or None"
            )

        if self.DD_SYSPASS_CLIENT_API_URL != DD_SYSPASS_CLIENT_API_URL:
            self.__DD_SYSPASS_CLIENT_API_URL = DD_SYSPASS_CLIENT_API_URL

    @property
    def DD_SYSPASS_CLIENT_API_VERSION(self):
        return self.__DD_SYSPASS_CLIENT_API_VERSION

    @DD_SYSPASS_CLIENT_API_VERSION.setter
    def DD_SYSPASS_CLIENT_API_VERSION(self, DD_SYSPASS_CLIENT_API_VERSION=None):
        if (
            DD_SYSPASS_CLIENT_API_VERSION is not None
            and type(DD_SYSPASS_CLIENT_API_VERSION) != str
            and type(DD_SYSPASS_CLIENT_API_VERSION) != AnsibleUnicode
            and type(DD_SYSPASS_CLIENT_API_VERSION) != AnsibleUnsafeText
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_API_VERSION' parameter, must be a str type or None"
            )

        if self.DD_SYSPASS_CLIENT_API_VERSION != DD_SYSPASS_CLIENT_API_VERSION:
            self.__DD_SYSPASS_CLIENT_API_VERSION = DD_SYSPASS_CLIENT_API_VERSION

    @property
    def DD_SYSPASS_CLIENT_DEBUG(self):
        return self.__DD_SYSPASS_CLIENT_DEBUG

    @DD_SYSPASS_CLIENT_DEBUG.setter
    def DD_SYSPASS_CLIENT_DEBUG(self, DD_SYSPASS_CLIENT_DEBUG=None):
        if DD_SYSPASS_CLIENT_DEBUG is None:
            DD_SYSPASS_CLIENT_DEBUG = False

        if (
            DD_SYSPASS_CLIENT_DEBUG is not None
            and type(DD_SYSPASS_CLIENT_DEBUG) != bool
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_DEBUG' parameter, must be a bool type or None"
            )

        if self.DD_SYSPASS_CLIENT_DEBUG != DD_SYSPASS_CLIENT_DEBUG:
            self.__DD_SYSPASS_CLIENT_DEBUG = DD_SYSPASS_CLIENT_DEBUG

    @property
    def DD_SYSPASS_CLIENT_DEBUG_LEVEL(self):
        return self.__DD_SYSPASS_CLIENT_DEBUG_LEVEL

    @DD_SYSPASS_CLIENT_DEBUG_LEVEL.setter
    def DD_SYSPASS_CLIENT_DEBUG_LEVEL(self, DD_SYSPASS_CLIENT_DEBUG_LEVEL=None):
        if DD_SYSPASS_CLIENT_DEBUG_LEVEL is None:
            DD_SYSPASS_CLIENT_DEBUG_LEVEL = 0

        if (
            DD_SYSPASS_CLIENT_DEBUG_LEVEL is not None
            and type(DD_SYSPASS_CLIENT_DEBUG_LEVEL) != int
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_DEBUG_LEVEL' parameter, must be a int type or None"
            )

        if self.DD_SYSPASS_CLIENT_DEBUG_LEVEL != DD_SYSPASS_CLIENT_DEBUG_LEVEL:
            self.__DD_SYSPASS_CLIENT_DEBUG_LEVEL = DD_SYSPASS_CLIENT_DEBUG_LEVEL

    @property
    def DD_SYSPASS_CLIENT_VERBOSE(self):
        return self.__DD_SYSPASS_CLIENT_VERBOSE

    @DD_SYSPASS_CLIENT_VERBOSE.setter
    def DD_SYSPASS_CLIENT_VERBOSE(self, DD_SYSPASS_CLIENT_VERBOSE=None):
        if DD_SYSPASS_CLIENT_VERBOSE is None:
            DD_SYSPASS_CLIENT_VERBOSE = False

        if (
            DD_SYSPASS_CLIENT_VERBOSE is not None
            and type(DD_SYSPASS_CLIENT_VERBOSE) != bool
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_VERBOSE' parameter, must be a bool type or None"
            )

        if self.DD_SYSPASS_CLIENT_VERBOSE != DD_SYSPASS_CLIENT_VERBOSE:
            self.__DD_SYSPASS_CLIENT_VERBOSE = DD_SYSPASS_CLIENT_VERBOSE
            if self.syspass_client:
                self.syspass_client.verbose = self.DD_SYSPASS_CLIENT_VERBOSE

    @property
    def DD_SYSPASS_CLIENT_VERBOSE_LEVEL(self):
        return self.__DD_SYSPASS_CLIENT_VERBOSE_LEVEL

    @DD_SYSPASS_CLIENT_VERBOSE_LEVEL.setter
    def DD_SYSPASS_CLIENT_VERBOSE_LEVEL(self, DD_SYSPASS_CLIENT_VERBOSE_LEVEL=None):
        if DD_SYSPASS_CLIENT_VERBOSE_LEVEL is None:
            DD_SYSPASS_CLIENT_VERBOSE_LEVEL = 0

        if (
            DD_SYSPASS_CLIENT_VERBOSE_LEVEL is not None
            and type(DD_SYSPASS_CLIENT_VERBOSE_LEVEL) != int
        ):
            raise TypeError(
                "'DD_SYSPASS_CLIENT_DEBUG_LEVEL' parameter, must be a int type or None"
            )

        if self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL != DD_SYSPASS_CLIENT_VERBOSE_LEVEL:
            self.__DD_SYSPASS_CLIENT_VERBOSE_LEVEL = DD_SYSPASS_CLIENT_VERBOSE_LEVEL

    @property
    def syspass_default_length(self):
        """
        The default password length use for generate password, use when password_length parameter is not set

        :return: The default password length
        :rtype: int
        """
        return self.__syspass_default_length

    @syspass_default_length.setter
    def syspass_default_length(self, value):
        """
        Set the default syspass_default_length in range [8..40]

        :param value: The default password length use for generate password
        :type value: int
        :raise TypeError: When  syspass_default_length is not in range 8 to 40
        """
        if type(value) != int:
            raise TypeError('"syspass_default_length" must be a int type')

        if value not in range(self.password_length_min, self.password_length_max + 1):
            raise ValueError(
                '"syspass_default_length" must be contain in range {0} to {1}'.format(
                    self.password_length_min, self.password_length_max
                )
            )

        if self.syspass_default_length != value:
            self.__syspass_default_length = value

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, account=None):
        """
        :param account: a account name
        :return: str or None
        """
        if account is None:
            raise TypeError('"Account" can not be none at all')

        if self.account != account:
            self.__account = account

    @property
    def password_length_min(self):
        return self.__password_length_min

    @password_length_min.setter
    def password_length_min(self, value):
        if type(value) != int:
            raise TypeError('"password_length_min" must be a int type')

        # Clamp value to 1
        if value < 1:
            value = 1
        # Fix a hard limit to 200, that the syspass 3.1 max
        if value >= 200:
            value = 199
        # Clamp value to max - 1
        if value >= self.password_length_max:
            value = self.password_length_max - 1

        if self.password_length_min != value:
            self.__password_length_min = value

    @property
    def password_length_max(self):
        return self.__password_length_max

    @password_length_max.setter
    def password_length_max(self, value):
        if type(value) != int:
            raise TypeError('"password_length_max" must be a int type')

        # Clamp value to 1
        if value < 1:
            value = 1
        # Clamp value to max - 1
        if value <= self.password_length_min:
            value = self.password_length_min + 1
        # Fix a hard limit to 200, that the syspass 3.1 max
        if value > 200:
            value = 200

        if self.password_length_max != value:
            self.__password_length_max = value

    @property
    def password_length(self):
        """
        The password length use to generate password.

        :return: The default password length
        :rtype: int
        """
        return self.__password_length

    @password_length.setter
    def password_length(self, value):
        """
        Set the password_length in range [8..40]

        :param value: The password length use to generate password
        :type value: int
        :raise TypeError: When  password_length is not in range 8 to 40
        """
        if type(value) != int:
            raise TypeError('"password_length" must be a int type')
        if value not in range(self.password_length_min, self.password_length_max + 1):
            raise ValueError(
                '"password_length" must be contain in range {0} to {1}'.format(
                    self.password_length_min, self.password_length_max
                )
            )

        if self.password_length != value:
            self.__password_length = value

    @property
    def chars(self):
        return self.__chars

    @chars.setter
    def chars(self, chars):
        if self.chars != chars:
            self.__chars = chars

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password=None):
        if password is None:
            self.gen_password()
            password = self.password

        if len(password) not in range(
            self.password_length_min, self.password_length_max + 1
        ):
            raise ValueError(
                '"password" must be contain in range {0} to {1}'.format(
                    self.password_length_min, self.password_length_max
                )
            )

        if self.password != password:
            self.__password = password

    @property
    def hostname(self):
        """
        hostname property

        :return:the hostname or None if haven't
        :rtype: str or None
        """
        return self.__hostname

    @hostname.setter
    def hostname(self, hostname):
        """
        Set the hostname property

        :param hostname: the hostname to set
        :type: or None
        """
        if (
            hostname is not None
            and type(hostname) != str
            and type(hostname) != AnsibleUnicode
            and type(hostname) != AnsibleUnsafeText
        ):
            raise TypeError('"hostname" must be a str or None')
        if self.hostname != hostname:
            self.__hostname = hostname

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, login=None):
        if (
            login is not None
            and type(login) != str
            and type(login) != AnsibleUnicode
            and type(login) != AnsibleUnsafeText
        ):
            raise TypeError('"login" must be a str or None')
        if self.login != login:
            self.__login = login

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, category=None):
        if (
            category is not None
            and type(category) != str
            and type(category) != AnsibleUnicode
            and type(category) != AnsibleUnsafeText
        ):
            raise TypeError('"category" must be a str or None')
        if self.category != category:
            self.__category = category

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, customer=None):
        if (
            customer is not None
            and type(customer) != str
            and type(customer) != AnsibleUnicode
            and type(customer) != AnsibleUnsafeText
        ):
            raise TypeError('"customer" must be a str or None')

        if self.customer != customer:
            self.__customer = customer

    @property
    def customer_desc(self):
        return self.__customer_desc

    @customer_desc.setter
    def customer_desc(self, customer_desc=None):
        if (
            customer_desc is not None
            and type(customer_desc) != str
            and type(customer_desc) != AnsibleUnicode
            and type(customer_desc) != AnsibleUnsafeText
        ):
            raise TypeError('"customer" must be a str or None')
        if customer_desc is None:
            customer_desc = ""
        if self.customer_desc != customer_desc:
            self.__customer_desc = customer_desc

    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags=None):
        if tags is not None and type(tags) != list:
            raise TypeError('"tags" must be a list or None')
        if tags is None:
            tags = []
        if self.tags != tags:
            self.__tags = tags

    @property
    def url(self):
        """
        Url from where access to the account

        :return: Account’s access URL or IP
        :rtype: str
        """
        return self.__url

    @url.setter
    def url(self, url=None):
        """
        Url from where access to the account

        if set to None url will be set to ""

        :param url: Account’s access URL or IP
        :type url: string or None
        """
        # if url is None:
        #     url = ""
        # print('URL')
        if (
            url is not None
            and type(url) != str
            and type(url) != AnsibleUnicode
            and type(url) != AnsibleUnsafeText
        ):
            raise TypeError('"url" must be a str or None')

        if self.url != url:
            self.__url = url

    @property
    def notes(self):
        return self.__notes

    @notes.setter
    def notes(self, notes=None):
        if (
            notes is not None
            and type(notes) != str
            and type(notes) != AnsibleUnicode
            and type(notes) != AnsibleUnsafeText
        ):
            raise TypeError('"notes" must be a str or None')
        if notes is None:
            notes = ""
        if self.notes != notes:
            self.__notes = notes

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state=None):
        if state is None:
            state = "present"
        if (
            type(state) != str
            and type(state) != AnsibleUnicode
            and type(state) != AnsibleUnsafeText
        ):
            raise TypeError('"state" must be a str or None')
        if str(state).lower() not in ["absent", "present"]:
            raise ValueError('"state" must be a "absent" or "present"')
        if self.state != str(state).lower():
            self.__state = str(state).lower()

    @property
    def private(self):
        """
        Set account as private. It can be either 0 or 1

        :return: 0 or 1
        :rtype: int
        """
        return self.__private

    @private.setter
    def private(self, private=None):
        if private is None:
            private = 0
        if type(private) != int:
            raise TypeError('"notes" private be a int or None')
        if private <= 0:
            private = 0
        if private >= 1:
            private = 1
        if self.private != private:
            self.__private = private

    @property
    def privategroup(self):
        """
        Set account as private for group. It can be either 0 or 1

        :return: 0 or 1
        :rtype: int
        """
        return self.__privategroup

    @privategroup.setter
    def privategroup(self, privategroup=None):
        if privategroup is not None and type(privategroup) != int:
            raise TypeError('"privategroup" private be a int or None')
        if privategroup is None:
            privategroup = 0
        if privategroup <= 0:
            privategroup = 0
        if privategroup >= 1:
            privategroup = 1
        if self.privategroup != privategroup:
            self.__privategroup = privategroup

    @property
    def expireDate(self):
        return self.__expireDate

    @expireDate.setter
    def expireDate(self, expireDate=None):
        if expireDate is None:
            expireDate = 0
        if type(expireDate) != int:
            raise TypeError('"expireDate" private be a int or None')

        if self.expireDate != expireDate:
            self.__expireDate = expireDate

    @property
    def ascii_letters(self):
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @property
    def digits(self):
        return "0123456789"

    @property
    def allowed_punctuation(self):
        return "-_|./?=+()[]~*{}#"

    def _gen_candidate_chars(self, characters=None):
        """
        Generate a string containing all valid chars as defined by ``characters``

        The values of each char spec can be:
        * a name of an attribute in the 'strings' module ('digits' for example).
        The value of the attribute will be added to the candidate chars.
        * a string of characters. If the string isn't an attribute in 'string'
        module, the string will be directly added to the candidate chars.

        By example::
        characters=['digits', '?|']``
        will match ``string.digits`` and add all ascii digits.  ``'?|'`` will add
        the question mark and pipe characters directly. Return will be the string::
        u'0123456789?|'

        :param characters: A list of character specs. The character specs are shorthand names for sets of characters \
        like 'digits', 'ascii_letters', or 'punctuation' or a string to be included verbatim.
        :type characters: list
        :return: str
        :rtype: str
        :raise TypeError: when ``characters``  is not a list
        """
        if type(characters) != list:
            raise TypeError("'characters' must be a list type")

        chars = ""
        if "ascii_letters" in characters:
            chars += self.ascii_letters
        if "digits" in characters:
            chars += self.digits
        if "allowed_punctuation" in characters:
            chars += self.allowed_punctuation

        if chars == "":
            raise ValueError("The password can not be generate with empty characters")

        return chars

    def _account_exist(self, text=None, matchall=None):
        """
        Test if a account exist

        :param text:
        :return: None if not exist else the JSon return of the syspassclient
        :rtype: None or dict
        """
        account_id = self.syspass_client.account_search(
            authToken=self.syspass_client.authToken, text=text, matchall=matchall
        )

        if account_id is not None and type(account_id) == int:
            return account_id
        else:
            return None

    def _account_create(self):
        """
        Internal function it create account without test if the account exist

        :return: the password of the account if it exist
        :rtype: str
        """

        # Following handlers verify existence of fields
        # creating them in case of absence.
        categoryId = self._ensure_category_id_exist()
        customerId = self._ensure_customer_id_exist()
        userGroupId = self._ensure_user_group_id_exist()
        tagsId = self._ensure_tags_id_exist()

        # if self.password is None:
        #     self.gen_password()

        self.syspass_client.account_create(
            authToken=self.syspass_client.authToken,
            tokenPass=self.syspass_client.tokenPass,
            name=self.account,
            categoryId=int(categoryId),
            clientId=int(customerId),
            userGroupId=int(userGroupId),
            password=self.password,
            login=self.login,
            url=self.url,
            tagsId=tagsId,
            notes=self.notes,
            privateGroup=self.privategroup,
            private=int(self.private),
            expireDate=self.expireDate,
            parentId=None,
        )

        return self.password

    def _account_exist_or_create(self):
        values = []

        account = self._account_exist(self.account)

        # if account is not None and isinstance(account, dict) and account["id"]:
        if account is not None and isinstance(account, int):
            if self.state == "absent":
                self.syspass_client.account_delete(
                    authToken=self.syspass_client.authToken, account_id=account
                )
                values_to_return = "Deleted Account"

            else:
                values_to_return = self.syspass_client.account_viewpass(
                    authToken=self.syspass_client.authToken, account_id=account
                )

        else:
            values_to_return = self._account_create()

        values.append(values_to_return)
        return values

    def _ensure_tags_id_exist(self, tags=None):
        if tags is None:
            tags = self.tags
        if type(tags) != list:
            raise TypeError('"tags" property and parameter can not be None')

        tagsId = []
        for tag in tags:
            returned_value = self.syspass_client.tag_search(
                authToken=self.syspass_client.authToken, text=tag
            )
            if returned_value is not None:
                tagsId.append(returned_value)
            else:
                tagsId.append(
                    self.syspass_client.tag_create(
                        authToken=self.syspass_client.authToken, name=tag
                    )
                )

        return tagsId

    def _ensure_user_group_id_exist(self, customer=None, customer_desc=None):
        if customer is None:
            customer = self.customer
        if (
            customer is not None
            and type(customer) != str
            and type(customer) != AnsibleUnicode
            and type(customer) != AnsibleUnsafeText
        ):
            raise TypeError('"customer" property and parameter can not be None')
        if customer == "":
            raise ValueError('"customer" property and parameter can not be empty')

        if customer_desc is None:
            customer_desc = self.customer_desc
        if (
            customer_desc is not None
            and type(customer_desc) != str
            and type(customer_desc) != AnsibleUnicode
            and type(customer_desc) != AnsibleUnsafeText
        ):
            raise TypeError('"customer_desc" property and parameter can not be None')

        userGroupId = self.syspass_client.user_group_search(
            authToken=self.syspass_client.authToken, text=customer, count=1
        )
        if userGroupId is None:
            if customer_desc is not None:
                userGroupId = self.syspass_client.user_group_create(
                    authToken=self.syspass_client.authToken,
                    name=customer,
                    description=customer_desc,
                )

            # #########################################################################################
            # #########################################################################################
            # ## Code impossible to touch, impossible to force, never that code is touch in any case ##
            # #########################################################################################
            # #########################################################################################
            # else:
            #     userGroupId = self.syspass_client.user_group_create(
            #         name=customer
            #     )
        return userGroupId

    def _ensure_customer_id_exist(self, customer=None):
        if customer is None:
            customer = self.customer
        if (
            type(customer) != str
            and type(customer) != AnsibleUnicode
            and type(customer) != AnsibleUnsafeText
        ):
            raise TypeError('"customer" property can not be None')
        if customer == "":
            raise ValueError('"customer" property can not be empty')

        customerId = self.syspass_client.client_search(
            authToken=self.syspass_client.authToken, text=customer
        )

        if customerId is None:
            customerId = self.syspass_client.client_create(
                authToken=self.syspass_client.authToken, name=customer
            )
        return customerId

    def _ensure_category_id_exist(self, category=None):
        if category is None:
            category = self.category
        if (
            category is not None
            and type(category) != str
            and type(category) != AnsibleUnicode
            and type(category) != AnsibleUnsafeText
        ):
            raise TypeError('"category" property can not be None')
        if category == "":
            raise ValueError('"category" property can not be empty')

        categoryId = self.syspass_client.category_search(
            authToken=self.syspass_client.authToken, text=category
        )
        if categoryId is None:
            categoryId = self.syspass_client.category_create(
                authToken=self.syspass_client.authToken, name=category
            )
        return categoryId

    def gen_password(self):
        """
        Function it generate a password

        :return: a password
        :rtype: str
        """

        password = " "
        if isinstance(self.params, dict) and "psswd_length" in self.params:
            self.password_length = self.params["psswd_length"]
        while " " in password:
            password = "{0}".format(
                "".join(
                    random.choice(str(self.chars)) for _ in range(self.password_length)
                )
            )

        self.password = password

    def _ensure_params(self):
        # global
        self._ensure_terms()
        self._ensure_variables()

        # syspass variables
        # self._ensure_syspass_API_URL()
        # self._ensure_syspass_API_KEY()
        # self._ensure_syspass_API_ACC_TOKPWD()

        # self.import_DD_SYSPASS_vars()

        # print("Force digdeo-syspass-client to be managed by the lookup")
        # self.syspass_client.api_url = self.DD_SYSPASS_CLIENT_API_URL
        # print("Force digdeo-syspass-client api_url to {0}".format(self.DD_SYSPASS_CLIENT_API_URL))
        # self.syspass_client.api_version = self.DD_SYSPASS_CLIENT_API_VERSION
        # self.syspass_client.authToken = self.DD_SYSPASS_CLIENT_AUTH_TOKEN
        # self.syspass_client.tokenPass = self.DD_SYSPASS_CLIENT_TOKEN_PASS
        # self.syspass_client.debug = self.DD_SYSPASS_CLIENT_DEBUG
        # self.syspass_client.debug_level = self.DD_SYSPASS_CLIENT_DEBUG_LEVEL
        # self.syspass_client.verbose = self.DD_SYSPASS_CLIENT_VERBOSE
        # self.syspass_client.verbose_level = self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL

        # specific parameters
        self._ensure_account()
        self._ensure_chars()
        self._ensure_password_length()
        self._ensure_password()
        self._ensure_hostname()
        self._ensure_login()
        self._ensure_category()
        self._ensure_customer()
        self._ensure_customer_desc()
        self._ensure_tags()
        self._ensure_url()
        self._ensure_notes()
        self._ensure_state()
        self._ensure_private()
        self._ensure_private_group()
        self._ensure_expiration_date()

        # Final
        self._ensure_everything_is_right()

        # In case term is a dict and not a string
        if isinstance(self.term, dict):
            if self.term.get("env", None) is not None:
                env = self.term.get("env")
                if env in ["prod", "prep", "rec", "dev", "tests"]:
                    if env.upper() not in self.tags:
                        self.tags.append(env.upper())

                self.url = self.term.get("url_listen")[0]
                self.login = self.term.get("login")
                self.account = "{0} {1} {2}".format(
                    self.hostname, self.login, self.category
                )
                ###############################
                #  WAS Comment   originally   #
                ###############################
                # self.customer = env.upper() #
                ###############################

            # elif self.term.get("app", None) is not None:
            elif "app" in self.term:
                if "APP" not in self.tags:
                    self.tags.append("APP")

                self.url = self.term.get("url_listen")[0]
                self.account = "{0} {1} {2}".format(
                    self.hostname, self.term["app"], self.category
                )

            if "state" in self.term:
                # if self.term.get("state", None) is not None:
                self.state = self.term.get("state")
                if "password" in self.term:
                    self.password = self.term.get("password")

    def import_DD_SYSPASS_vars(self):
        if self.debug and self.debug_level > 1:
            print(
                Fore.YELLOW
                + Style.BRIGHT
                + "{0}: ".format(self.__class__.__name__.upper()),
                end="",
            )
            print(
                Fore.WHITE
                + Style.BRIGHT
                + "{0}".format("Import DD_SYSPASS_CLIENT vars")
            )

        self._ensure_DD_SYSPASS_CLIENT_API_URL()
        self._ensure_DD_SYSPASS_CLIENT_API_VERSION()
        self._ensure_DD_SYSPASS_CLIENT_AUTH_TOKEN()
        self._ensure_DD_SYSPASS_CLIENT_DEBUG()
        self._ensure_DD_SYSPASS_CLIENT_DEBUG_LEVEL()
        self._ensure_DD_SYSPASS_CLIENT_VERBOSE()
        self._ensure_DD_SYSPASS_CLIENT_VERBOSE_LEVEL()
        self._ensure_DD_SYSPASS_CLIENT_VERIFY_SSL()
        self._ensure_DD_SYSPASS_CLIENT_TOKEN_PASS()

    def impose_DD_SYSPASS_vars(self):

        if self.syspass_client:
            if self.debug and self.debug_level > 1:
                # Title
                print(
                    Fore.YELLOW
                    + Style.BRIGHT
                    + "{0}: ".format(self.__class__.__name__.upper()),
                    end="",
                )
                print(
                    Fore.WHITE
                    + Style.BRIGHT
                    + "{0} {1}".format("Impose setting to", self.syspass_client)
                )

            # DD_SYSPASS_CLIENT_API_URL
            self.syspass_client.api_url = self.DD_SYSPASS_CLIENT_API_URL
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_API_URL:",
                    end="",
                )
                if self.DD_SYSPASS_CLIENT_API_URL == self.syspass_client.api_url:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_API_VERSION
            self.syspass_client.api_version = self.DD_SYSPASS_CLIENT_API_VERSION
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_API_VERSION:",
                    end="",
                )
                if (
                    self.DD_SYSPASS_CLIENT_API_VERSION
                    == self.syspass_client.api_version
                ):
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_AUTH_TOKEN
            self.syspass_client.authToken = self.DD_SYSPASS_CLIENT_AUTH_TOKEN
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_AUTH_TOKEN:",
                    end="",
                )
                if self.DD_SYSPASS_CLIENT_AUTH_TOKEN == self.syspass_client.authToken:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_DEBUG
            self.syspass_client.debug = self.DD_SYSPASS_CLIENT_DEBUG
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_DEBUG:",
                    end="",
                )
                if self.DD_SYSPASS_CLIENT_DEBUG == self.syspass_client.debug:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_DEBUG_LEVEL
            self.syspass_client.debug_level = self.DD_SYSPASS_CLIENT_DEBUG_LEVEL
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_DEBUG_LEVEL:",
                    end="",
                )
                if (
                    self.DD_SYSPASS_CLIENT_DEBUG_LEVEL
                    == self.syspass_client.debug_level
                ):
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_VERBOSE
            self.syspass_client.verbose = self.DD_SYSPASS_CLIENT_VERBOSE
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_VERBOSE:",
                    end="",
                )
                if self.DD_SYSPASS_CLIENT_VERBOSE == self.syspass_client.verbose:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_VERBOSE_LEVEL
            self.syspass_client.verbose_level = self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_VERBOSE_LEVEL:",
                    end="",
                )
                if (
                    self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL
                    == self.syspass_client.verbose_level
                ):
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_VERIFY_SSL
            self.syspass_client.verify_ssl = self.DD_SYSPASS_CLIENT_VERIFY_SSL
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_VERIFY_SSL:",
                    end="",
                )
                if self.DD_SYSPASS_CLIENT_VERIFY_SSL == self.syspass_client.verify_ssl:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

            # DD_SYSPASS_CLIENT_TOKEN_PASS
            self.syspass_client.tokenPass = self.DD_SYSPASS_CLIENT_TOKEN_PASS
            if self.debug and self.debug_level > 2:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + "> "
                    + Fore.WHITE
                    + "DD_SYSPASS_CLIENT_TOKEN_PASS:",
                    end="",
                )
                if self.DD_SYSPASS_CLIENT_TOKEN_PASS == self.syspass_client.tokenPass:
                    print(Fore.GREEN + Style.BRIGHT + " {0}".format("OK"))
                else:  # pragma: no cover
                    print(Fore.RED + Style.BRIGHT + " {0}".format("FAILED"))

    def _ensure_everything_is_right(self):
        self.params = {
            "chars": self.chars,
            "psswd_length": self.password_length,
            "password": self.password,
            "hostname": self.hostname,
            "account": self.account,
            "login": self.login,
            "category": self.category,
            "customer": self.customer,
            "customer_desc": self.customer_desc,
            "tags": self.tags,
            "url": self.url,
            "notes": self.notes,
            "state": self.state,
            "private": self.private,
            "privategroup": self.privategroup,
            "expireDate": self.expireDate,
        }
        for k, v in self.params.items():
            if v is None:
                if k == "url":
                    pass
                else:
                    raise ValueError("Error : %s must be defined" % k)

    def _ensure_account(self):
        self.account = self.term

    def _ensure_category(self):
        # category
        if isinstance(self.kwargs, dict) and "category" in self.kwargs:
            self.category = self.kwargs["category"]

    def _ensure_customer(self):
        # customer
        if isinstance(self.kwargs, dict) and "customer" in self.kwargs:
            self.customer = self.kwargs["customer"]

    def _ensure_customer_desc(self):
        # customer_desc
        if isinstance(self.kwargs, dict) and "customer_desc" in self.kwargs:
            self.customer_desc = self.kwargs["customer_desc"]

    def _ensure_chars(self):
        # chars
        if isinstance(self.kwargs, dict) and "chars" in self.kwargs:
            self.chars = self._gen_candidate_chars(self.kwargs["chars"])

    def _ensure_expiration_date(self):
        # expirationDate
        if isinstance(self.kwargs, dict) and "expireDate" in self.kwargs:
            self.expireDate = self.kwargs["expireDate"]

    def _ensure_hostname(self):
        # hostname
        if self.variables is not None:
            if isinstance(self.variables, dict) and "host_override" in self.variables:
                self.hostname = str(self.variables["host_override"])
            elif (
                isinstance(self.variables, dict)
                and "ansible_hostname" in self.variables
            ):
                self.hostname = str(self.variables["ansible_hostname"].split(".")[0])

    def _ensure_login(self):
        # login
        if isinstance(self.kwargs, dict) and "login" in self.kwargs:
            self.login = self.kwargs["login"]
        elif isinstance(self.term, dict):
            self.login = ""

    def _ensure_notes(self):
        # notes
        if isinstance(self.kwargs, dict) and "notes" in self.kwargs:
            self.notes = self.kwargs["notes"]

    def _ensure_password(self):
        # password
        if isinstance(self.params, dict) and "password" in self.params:
            if self.params["password"] is not None and self.params["password"] != "":
                self.password = self.params["password"]
        else:
            self.gen_password()

    def _ensure_password_length(self):
        # password length
        if isinstance(self.kwargs, dict) and "psswd_length" in self.kwargs:
            self.password_length = self.kwargs["psswd_length"]
        elif (
            isinstance(self._templar, dict) and "_available_variables" in self._templar
        ):
            if "syspass_default_length" in self._templar["_available_variables"]:
                self.password_length = int(
                    self._templar["_available_variables"]["syspass_default_length"]
                )

    def _ensure_private(self):
        # private
        if isinstance(self.kwargs, dict) and "private" in self.kwargs:
            if type(self.kwargs["private"]) == bool:
                if self.kwargs["private"] is True:
                    self.private = 1
                else:
                    self.private = 0
            else:
                self.private = 0

    def _ensure_private_group(self):
        # privategroup
        if isinstance(self.kwargs, dict) and "privategroup" in self.kwargs:
            if type(self.kwargs["privategroup"]) == bool:
                if self.kwargs["privategroup"] is True:
                    self.privategroup = 1
                else:
                    self.privategroup = 0
            else:
                self.privategroup = 0

    def _ensure_state(self):
        self.state = "present"

        if isinstance(self.kwargs, dict) and "state" in self.kwargs:
            if self.kwargs["state"] is not None:
                self.state = self.kwargs["state"]

        if isinstance(self.term, dict) and "state" in self.term:
            if self.term["state"] is not None:
                self.state = self.term["state"]

    def _ensure_DD_SYSPASS_CLIENT_AUTH_TOKEN(self):
        # DD_SYSPASS_CLIENT_AUTH_TOKEN
        if (
            isinstance(self.kwargs, dict)
            and "DD_SYSPASS_CLIENT_AUTH_TOKEN" in self.kwargs
        ):
            self.DD_SYSPASS_CLIENT_AUTH_TOKEN = str(
                self.kwargs["DD_SYSPASS_CLIENT_AUTH_TOKEN"]
            )
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_AUTH_TOKEN" in self._templar["_available_variables"]
        ):
            self.DD_SYSPASS_CLIENT_AUTH_TOKEN = str(
                self._templar["_available_variables"]["DD_SYSPASS_CLIENT_AUTH_TOKEN"]
            )
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_AUTH_TOKEN" in self.variables
        ):
            self.DD_SYSPASS_CLIENT_AUTH_TOKEN = str(
                self.variables["DD_SYSPASS_CLIENT_AUTH_TOKEN"]
            )

        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_AUTH_TOKEN: ",
                end="",
            )
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "{0}".format(self.DD_SYSPASS_CLIENT_AUTH_TOKEN)
            )

    def _ensure_DD_SYSPASS_CLIENT_TOKEN_PASS(self):
        # DD_SYSPASS_CLIENT_TOKEN_PASS
        if (
            isinstance(self.kwargs, dict)
            and "DD_SYSPASS_CLIENT_TOKEN_PASS" in self.kwargs
        ):
            self.DD_SYSPASS_CLIENT_TOKEN_PASS = str(
                self.kwargs["DD_SYSPASS_CLIENT_TOKEN_PASS"]
            )
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_TOKEN_PASS" in self._templar["_available_variables"]
        ):
            self.DD_SYSPASS_CLIENT_TOKEN_PASS = str(
                self._templar["_available_variables"]["DD_SYSPASS_CLIENT_TOKEN_PASS"]
            )
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_TOKEN_PASS" in self.variables
        ):
            self.DD_SYSPASS_CLIENT_TOKEN_PASS = str(
                self.variables["DD_SYSPASS_CLIENT_TOKEN_PASS"]
            )
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_TOKEN_PASS: ",
                end="",
            )
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "{0}".format(self.DD_SYSPASS_CLIENT_TOKEN_PASS)
            )

    def _ensure_DD_SYSPASS_CLIENT_VERIFY_SSL(self):
        # DD_SYSPASS_CLIENT_VERIFY_SSL
        if (
            isinstance(self.kwargs, dict)
            and "DD_SYSPASS_CLIENT_VERIFY_SSL" in self.kwargs
        ):
            if (
                str(self.kwargs["DD_SYSPASS_CLIENT_VERIFY_SSL"]).lower() == "true"
                or str(self.kwargs["DD_SYSPASS_CLIENT_VERIFY_SSL"]).lower() == "yes"
            ):
                self.DD_SYSPASS_CLIENT_VERIFY_SSL = True
            else:
                self.DD_SYSPASS_CLIENT_VERIFY_SSL = False

        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_VERIFY_SSL" in self._templar["_available_variables"]
        ):
            if (
                str(
                    self._templar["_available_variables"][
                        "DD_SYSPASS_CLIENT_VERIFY_SSL"
                    ]
                ).lower()
                == "true"
                or str(
                    self._templar["_available_variables"][
                        "DD_SYSPASS_CLIENT_VERIFY_SSL"
                    ]
                ).lower()
                == "yes"
            ):
                self.DD_SYSPASS_CLIENT_VERIFY_SSL = True
            else:
                self.DD_SYSPASS_CLIENT_VERIFY_SSL = False

        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_VERIFY_SSL" in self.variables
        ):
            if (
                str(self.variables["DD_SYSPASS_CLIENT_VERIFY_SSL"]).lower() == "true"
                or str(self.variables["DD_SYSPASS_CLIENT_VERIFY_SSL"]).lower() == "yes"
            ):
                self.DD_SYSPASS_CLIENT_VERIFY_SSL = True
            else:
                self.DD_SYSPASS_CLIENT_VERIFY_SSL = False

        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_VERIFY_SSL: ",
                end="",
            )
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "{0}".format(self.DD_SYSPASS_CLIENT_VERIFY_SSL)
            )

    def _ensure_DD_SYSPASS_CLIENT_API_URL(self):
        # DD_SYSPASS_CLIENT_API_URL
        if isinstance(self.kwargs, dict) and "DD_SYSPASS_CLIENT_API_URL" in self.kwargs:
            self.DD_SYSPASS_CLIENT_API_URL = str(
                self.kwargs["DD_SYSPASS_CLIENT_API_URL"]
            )
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_API_URL" in self._templar["_available_variables"]
        ):
            self.DD_SYSPASS_CLIENT_API_URL = str(
                self._templar["_available_variables"]["DD_SYSPASS_CLIENT_API_URL"]
            )
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_API_URL" in self.variables
        ):
            self.DD_SYSPASS_CLIENT_API_URL = str(
                self.variables["DD_SYSPASS_CLIENT_API_URL"]
            )
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_API_URL: ",
                end="",
            )
            print(
                Fore.GREEN + Style.BRIGHT + "{0}".format(self.DD_SYSPASS_CLIENT_API_URL)
            )

    def _ensure_DD_SYSPASS_CLIENT_API_VERSION(self):
        # DD_SYSPASS_CLIENT_API_VERSION
        if (
            isinstance(self.kwargs, dict)
            and "DD_SYSPASS_CLIENT_API_VERSION" in self.kwargs
        ):
            self.DD_SYSPASS_CLIENT_API_VERSION = str(
                self.kwargs["DD_SYSPASS_CLIENT_API_VERSION"]
            )
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_API_VERSION" in self._templar["_available_variables"]
        ):
            self.DD_SYSPASS_CLIENT_API_VERSION = str(
                self._templar["_available_variables"]["DD_SYSPASS_CLIENT_API_VERSION"]
            )
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_API_VERSION" in self.variables
        ):
            self.DD_SYSPASS_CLIENT_API_VERSION = str(
                self.variables["DD_SYSPASS_CLIENT_API_VERSION"]
            )
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_API_VERSION: ",
                end="",
            )
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "{0}".format(self.DD_SYSPASS_CLIENT_API_VERSION)
            )

    def _ensure_DD_SYSPASS_CLIENT_DEBUG(self):
        # DD_SYSPASS_CLIENT_DEBUG
        if isinstance(self.kwargs, dict) and "DD_SYSPASS_CLIENT_DEBUG" in self.kwargs:
            if (
                str(self.kwargs["DD_SYSPASS_CLIENT_DEBUG"]).lower() == "true"
                or str(self.kwargs["DD_SYSPASS_CLIENT_DEBUG"]).lower() == "yes"
            ):
                self.DD_SYSPASS_CLIENT_DEBUG = True
            else:
                self.DD_SYSPASS_CLIENT_DEBUG = False
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_DEBUG" in self._templar["_available_variables"]
        ):
            if (
                str(
                    self._templar["_available_variables"]["DD_SYSPASS_CLIENT_DEBUG"]
                ).lower()
                == "true"
                or str(
                    self._templar["_available_variables"]["DD_SYSPASS_CLIENT_DEBUG"]
                ).lower()
                == "yes"
            ):
                self.DD_SYSPASS_CLIENT_DEBUG = True
            else:
                self.DD_SYSPASS_CLIENT_DEBUG = False
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_DEBUG" in self.variables
        ):
            if (
                str(self.variables["DD_SYSPASS_CLIENT_DEBUG"]).lower() == "true"
                or str(self.variables["DD_SYSPASS_CLIENT_DEBUG"]).lower() == "yes"
            ):
                self.DD_SYSPASS_CLIENT_DEBUG = True
            else:
                self.DD_SYSPASS_CLIENT_DEBUG = False
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_DEBUG: ",
                end="",
            )
            print(
                Fore.GREEN + Style.BRIGHT + "{0}".format(self.DD_SYSPASS_CLIENT_DEBUG)
            )

    def _ensure_DD_SYSPASS_CLIENT_DEBUG_LEVEL(self):
        # DD_SYSPASS_CLIENT_DEBUG_LEVEL
        if (
            isinstance(self.kwargs, dict)
            and "DD_SYSPASS_CLIENT_DEBUG_LEVEL" in self.kwargs
        ):
            self.DD_SYSPASS_CLIENT_DEBUG_LEVEL = int(
                self.kwargs["DD_SYSPASS_CLIENT_DEBUG_LEVEL"]
            )
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_DEBUG_LEVEL" in self._templar["_available_variables"]
        ):
            self.DD_SYSPASS_CLIENT_DEBUG_LEVEL = int(
                self._templar["_available_variables"]["DD_SYSPASS_CLIENT_DEBUG_LEVEL"]
            )
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_DEBUG_LEVEL" in self.variables
        ):
            self.DD_SYSPASS_CLIENT_DEBUG_LEVEL = int(
                self.variables["DD_SYSPASS_CLIENT_DEBUG_LEVEL"]
            )
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_DEBUG_LEVEL: ",
                end="",
            )
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "{0}".format(self.DD_SYSPASS_CLIENT_DEBUG_LEVEL)
            )

    def _ensure_DD_SYSPASS_CLIENT_VERBOSE(self):
        # DD_SYSPASS_CLIENT_VERBOSE
        if isinstance(self.kwargs, dict) and "DD_SYSPASS_CLIENT_VERBOSE" in self.kwargs:
            if (
                str(self.kwargs["DD_SYSPASS_CLIENT_VERBOSE"]).lower() == "true"
                or str(self.kwargs["DD_SYSPASS_CLIENT_VERBOSE"]).lower() == "yes"
            ):
                self.DD_SYSPASS_CLIENT_VERBOSE = True
            else:
                self.DD_SYSPASS_CLIENT_VERBOSE = False
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_VERBOSE" in self._templar["_available_variables"]
        ):
            if (
                str(
                    self._templar["_available_variables"]["DD_SYSPASS_CLIENT_VERBOSE"]
                ).lower()
                == "true"
                or str(
                    self._templar["_available_variables"]["DD_SYSPASS_CLIENT_VERBOSE"]
                ).lower()
                == "yes"
            ):
                self.DD_SYSPASS_CLIENT_VERBOSE = True
            else:
                self.DD_SYSPASS_CLIENT_VERBOSE = False
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_VERBOSE" in self.variables
        ):
            if (
                str(self.variables["DD_SYSPASS_CLIENT_VERBOSE"]).lower() == "true"
                or str(self.variables["DD_SYSPASS_CLIENT_VERBOSE"]).lower() == "yes"
            ):
                self.DD_SYSPASS_CLIENT_VERBOSE = True
            else:
                self.DD_SYSPASS_CLIENT_VERBOSE = False
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_VERBOSE: ",
                end="",
            )
            print(
                Fore.GREEN + Style.BRIGHT + "{0}".format(self.DD_SYSPASS_CLIENT_VERBOSE)
            )

    def _ensure_DD_SYSPASS_CLIENT_VERBOSE_LEVEL(self):
        # DD_SYSPASS_CLIENT_VERBOSE_LEVEL
        if (
            isinstance(self.kwargs, dict)
            and "DD_SYSPASS_CLIENT_VERBOSE_LEVEL" in self.kwargs
        ):
            self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL = int(
                self.kwargs["DD_SYSPASS_CLIENT_VERBOSE_LEVEL"]
            )
        elif (
            isinstance(self._templar, dict)
            and "_available_variables" in self._templar
            and "DD_SYSPASS_CLIENT_VERBOSE_LEVEL"
            in self._templar["_available_variables"]
        ):
            self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL = int(
                self._templar["_available_variables"]["DD_SYSPASS_CLIENT_VERBOSE_LEVEL"]
            )
        elif (
            isinstance(self.variables, dict)
            and "DD_SYSPASS_CLIENT_VERBOSE_LEVEL" in self.variables
        ):
            self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL = int(
                self.variables["DD_SYSPASS_CLIENT_VERBOSE_LEVEL"]
            )
        if self.debug and self.debug_level > 1:
            print(
                Fore.CYAN
                + Style.BRIGHT
                + "< "
                + Fore.WHITE
                + "DD_SYSPASS_CLIENT_VERBOSE_LEVEL: ",
                end="",
            )
            print(
                Fore.GREEN
                + Style.BRIGHT
                + "{0}".format(self.DD_SYSPASS_CLIENT_VERBOSE_LEVEL)
            )

    def _ensure_tags(self):
        # tags
        if isinstance(self.kwargs, dict) and "tags" in self.kwargs:
            self.tags = self.kwargs["tags"]

    def _ensure_url(self):
        # url
        if type(self.kwargs) == dict and "url" in self.kwargs:
            self.url = self.kwargs["url"]

        if type(self.term) == dict and "url_listen" in self.term:
            self.url = self.term["url_listen"][0]

    def _ensure_variables(self):
        if self.variables is not None:  # pragma: no cover
            if self._templar is not None:
                if hasattr(self._templar, "_available_variables"):
                    self._templar._available_variables = self.variables

    @property
    def term(self):
        return self.__term

    @term.setter
    def term(self, term=None):
        if (
            term is not None
            and type(term) != str
            and type(term) != AnsibleUnicode
            and type(term) != AnsibleUnsafeText
            and type(term) != list
            and type(term) != dict
        ):
            raise TypeError('"term" must be a None, str or dict type')

        if isinstance(term, list):
            term = term[0]

        # if term is not None and type(term) != dict and type(term) != list:
        #     term = ''
        # if isinstance(self.term, dict):
        #     self.term = term
        # if isinstance(term, list) and len(term) == 1:
        #     term = dict(term[0])
        # else:
        #     raise AnsibleError("Term is not correct Error : %s" % self.term)
        if term != self.term:
            self.__term = term

    @property
    def variables(self):
        return self.__variables

    @variables.setter
    def variables(self, variables=None):
        if variables is None:
            variables = {}
        if type(variables) != dict:
            raise TypeError("'variables' MUST be a dict type")
        if variables != self.variables:
            self.__variables = variables

    @property
    def kwargs(self):
        return self.__kwargs

    @kwargs.setter
    def kwargs(self, value=None):
        if value is None:
            value = {}
        if type(value) != dict:
            raise TypeError('"kwargs" must be a dict type')
        if "kwargs" in value:
            value = value["kwargs"]
        if value != self.kwargs:
            self.__kwargs = value

    @property
    def params(self):
        return self.__params

    @params.setter
    def params(self, params=None):
        """

        :param params:
        :type params: dict or None
        """
        if params is None:
            self.__params = {}
        if params != self.params:
            self.__params = params

    def run(self, term, variables=None, **kwargs):
        """

        :param term: the first argument is a list containing the terms.
        :type term: list or str
        :param variables:
        :param kwargs:
        :return:
        """
        # Import everything
        self.term = term
        self.variables = variables
        self.kwargs = kwargs

        # Process parameters
        self._ensure_params()
        self.import_DD_SYSPASS_vars()
        self.impose_DD_SYSPASS_vars()

        # self.syspass_client.config_read_file()
        # self.syspass_client.api_read_file()
        self.syspass_client.display_resume()

        # Make the work
        return self._account_exist_or_create()

    def _ensure_terms(self):
        pass
        # Small code for know if the first argument is a string or a list element.

        # if isinstance(self.term, dict):
        #     self.term = dict(self.term)
        # elif len(self.term) == 1:
        #     self.term = self.term[0]
        #
        # if isinstance(self.term, dict):
        #     pass
        # elif isinstance(self.term, str):
        #     pass
        # elif isinstance(self.term, list) and len(self.term) == 1:
        #     self.term = self.term[0]
        # else:
        #     raise AnsibleError("Term is not correct Error : %s" % self.term)


# def main():
#     sys.stdout.write(LookupModule().run(sys.argv[1:], None)[0])
#     sys.stdout.write("\n")
#     sys.stdout.flush()
#     return 0


# if __name__ == "__main__":
#     sys.exit(main())
