# -*- coding: utf-8 -*-
# Copyright (c) 2020 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.

from typing import List, Optional, Tuple, Union
from typing_extensions import TypedDict

PromptedCommand = TypedDict('PromptedCommand', {
    'cmd': str,
    'input': str
})

Command = Union[str, PromptedCommand]

Params = TypedDict('Params', {
    'version': int,
    'cmds': List[Command],
    'format': str,
    'timestamps': bool,
	'auto_complete': bool,
	'expand_aliases': bool,
	'include_error_detail': bool,
	'streaming': bool # not support until 4.24
}, total=False)

Request = TypedDict('Request', {
    'id': str,
    'jsonrpc': str,
    'method': str,
    'streaming': bool, # eAPI hack
    'params': Params
}, total=False)


Auth = Tuple[str, Optional[str]]

Certificate = Optional[Union[str, Tuple[str, str], Tuple[str, str, str]]]

Timeout = Union[None, float, Tuple[float, float, float, float]]

# RequestsOptions = TypedDict('RequestsOptions', {
#     'auth': Auth,
#     'timeout': Timeout,
#     'cert': Certificate,
#     'verify': bool
# }, total=False)
