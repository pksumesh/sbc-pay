# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Error definitions."""
from enum import Enum
from http import HTTPStatus


class Error(Enum):
    """Error Codes."""

    PAY001 = 'Invalid Corp Type or Filing Type', HTTPStatus.BAD_REQUEST
    PAY002 = 'No matching record found for Corp Type and Filing Type', HTTPStatus.BAD_REQUEST

    def __new__(cls, message, status):
        obj = object.__new__(cls)
        obj.message = message
        obj.status = status
        return obj
