# Copyright 2020 KT AI Lab.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
agent - AI Kit Python Library
"""

__title__ = 'agent'
__version__ = '1.0.0'
__author__ = 'CheolMin Lee, JinHyeon An'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright (c) 2018-2020 KT AI Lab.'
VERSION = tuple(map(int, __version__.split('.')))

from .service import *
from .regist import *
from .logout import *
from ._authorize import *
from .grpc_channel import *

