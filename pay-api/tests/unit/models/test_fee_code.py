# Copyright © 2019 Province of British Columbia
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

"""Tests to assure the FeeCode Class.

Test-Suite to ensure that the FeeCode Class is working as expected.
"""
import datetime

from pay_api.models import FeeCode


def factory_feecode(fee_code: str, amount: int):
    """Return a valid FeeCode object."""
    return FeeCode(fee_code=fee_code,
                   amount=amount)


def test_feecode(session):
    """Assert a valid fee code is stored correctly.

    Start with a blank database.
    """
    feecode = factory_feecode('EN101', 100)
    feecode.save()

    assert feecode.fee_code is not None


def test_feecode_find_by_fee_code(session):
    """Assert that the feecode can be found by code."""
    feecode = factory_feecode('EN101', 100)
    session.add(feecode)
    session.commit()

    b = FeeCode.find_by_fee_code('EN101')
    assert b is not None


def test_feecode_find_by_invalid_fee_code(session):
    """Assert that the feecode can not be found, with invalid code"""
    feecode = factory_feecode('EN101', 100)
    session.add(feecode)
    session.commit()

    b = FeeCode.find_by_fee_code('EN102')
    assert b is None
