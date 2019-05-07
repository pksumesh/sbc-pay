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

"""Tests to assure the fees end-point.

Test-Suite to ensure that the /fees endpoint is working as expected.
"""
import json
from pay_api.models import CorpType, FeeCode, FilingType, FeeSchedule
from datetime import date, timedelta
from pay_api.utils.roles import Role

token_header = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "sbc-auth-cron-job"
}

def get_claims(role:str = Role.BASIC.value):
    claim = {
        "jti": "a50fafa4-c4d6-4a9b-9e51-1e5e0d102878",
        "exp": 1557273180,
        "nbf": 0,
        "iat": 1557269580,
        "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/fcf0kpqr",
        "aud": "sbc-auth-web",
        "sub": "15099883-3c3f-4b4c-a124-a1824d6cba84",
        "typ": "Bearer",
        "azp": "sbc-auth-web",
        "auth_time": 0,
        "session_state": "f1d8636b-e4a9-4f75-a204-6b3e2d395fb1",
        "acr": "1",
        "realm_access":
            {
                "roles":
                    [
                        "{}".format(role)
                    ]
            }
    }
    return claim


def test_fees_with_corp_type_and_filing_type(session, client, jwt, app):
    """Assert that the endpoint returns 200."""
    token = jwt.create_jwt(get_claims(), token_header)
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}
    corp_type = 'XX'
    filing_type_code = 'XOTANN'
    factory_fee_schedule_model(
        factory_filing_type_model('XOTANN', 'TEST'),
        factory_corp_type_model('XX', 'TEST'),
        factory_fee_model('XXX', 100))
    rv = client.get(f'/api/v1/fees/{corp_type}/{filing_type_code}', headers=headers)
    assert rv.status_code == 200


def test_fees_with_corp_type_and_filing_type_with_valid_start_date(session, client, jwt, app):
    """Assert that the endpoint returns 200."""
    # Insert a record first and then query for it
    token = jwt.create_jwt(get_claims(), token_header)
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}

    corp_type = 'XX'
    filing_type_code = 'XOTANN'
    now = date.today()
    factory_fee_schedule_model(
        factory_filing_type_model('XOTANN', 'TEST'),
        factory_corp_type_model('XX', 'TEST'),
        factory_fee_model('XXX', 100),
        now - timedelta(1))
    rv = client.get(f'/api/v1/fees/{corp_type}/{filing_type_code}?valid_date={now}', headers=headers)
    assert rv.status_code == 200


def test_fees_with_corp_type_and_filing_type_with_invalid_start_date(session, client, jwt, app):
    """Assert that the endpoint returns 400."""
    # Insert a record first and then query for it
    token = jwt.create_jwt(get_claims(), token_header)
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}

    corp_type = 'XX'
    filing_type_code = 'XOTANN'
    now = date.today()
    factory_fee_schedule_model(
        factory_filing_type_model('XOTANN', 'TEST'),
        factory_corp_type_model('XX', 'TEST'),
        factory_fee_model('XXX', 100),
        now + timedelta(1))
    rv = client.get(f'/api/v1/fees/{corp_type}/{filing_type_code}?valid_date={now}', headers=headers)
    assert rv.status_code == 400


def test_fees_with_corp_type_and_filing_type_with_valid_end_date(session, client, jwt, app):
    """Assert that the endpoint returns 200."""
    # Insert a record first and then query for it
    token = jwt.create_jwt(get_claims(), token_header)
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}

    corp_type = 'XX'
    filing_type_code = 'XOTANN'
    now = date.today()
    factory_fee_schedule_model(
        factory_filing_type_model('XOTANN', 'TEST'),
        factory_corp_type_model('XX', 'TEST'),
        factory_fee_model('XXX', 100),
        now - timedelta(1),
        now)
    rv = client.get(f'/api/v1/fees/{corp_type}/{filing_type_code}?valid_date={now}', headers=headers)
    assert rv.status_code == 200


def test_fees_with_corp_type_and_filing_type_with_invalid_end_date(session, client, jwt, app):
    """Assert that the endpoint returns 400."""
    # Insert a record first and then query for it
    token = jwt.create_jwt(get_claims(), token_header)
    headers = {'Authorization': f'Bearer {token}', 'content-type': 'application/json'}

    corp_type = 'XX'
    filing_type_code = 'XOTANN'
    now = date.today()
    factory_fee_schedule_model(
        factory_filing_type_model('XOTANN', 'TEST'),
        factory_corp_type_model('XX', 'TEST'),
        factory_fee_model('XXX', 100),
        now - timedelta(2),
        now - timedelta(1))
    rv = client.get(f'/api/v1/fees/{corp_type}/{filing_type_code}?valid_date={now}', headers=headers)
    assert rv.status_code == 400


def factory_filing_type_model(
        filing_type_code: str,
        filing_description: str = 'TEST'):
    filing_type = FilingType(filing_type_code=filing_type_code,
                             filing_description=filing_description)
    filing_type.save()
    return filing_type


def factory_fee_model(
        fee_code: str,
        amount: int):
    fee_code_master = FeeCode(fee_code=fee_code,
                              amount=amount)
    fee_code_master.save()
    return fee_code_master


def factory_corp_type_model(
        corp_type_code: str,
        corp_type_description: str):
    corp_type = CorpType(corp_type_code=corp_type_code,
                         corp_type_description=corp_type_description)
    corp_type.save()
    return corp_type


def factory_fee_schedule_model(
        filing_type: FilingType,
        corp_type: CorpType,
        fee_code: FeeCode,
        fee_start_date: date = date.today(),
        fee_end_date: date = None):
    fee_schedule = FeeSchedule(filing_type_code=filing_type.filing_type_code,
                               corp_type_code=corp_type.corp_type_code,
                               fee_code=fee_code.fee_code,
                               fee_start_date=fee_start_date,
                               fee_end_date=fee_end_date)
    fee_schedule.save()
    return fee_schedule


