# Copyright 2024 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

from jose import jwt
import pytest

from maasserver.models import Config
from maasserver.msm import (
    ACCESS,
    AUDIENCE,
    ENROLMENT,
    msm_enrol,
    msm_status,
    MSMException,
)
from maasserver.secrets import SecretManager

TOKEN_ALGORITHM = "HS256"
TOKEN_DURATION = timedelta(minutes=10)


@pytest.fixture
def maas_site(factory):
    settings = {
        "maas_name": factory.make_name(prefix="maas"),
        "maas_url": factory.make_simple_http_url(path="/MAAS"),
    }
    for k, v in settings.items():
        Config.objects.set_config(k, v)
    yield settings


@pytest.fixture
def msm_site(factory):
    site = factory.make_simple_http_url()
    yield site


@pytest.fixture
def msm_enrol_payload(factory, msm_site):
    enrol_url = urlparse(msm_site)._replace(path="/site/v1/enrol").geturl()
    issued = datetime.now(timezone.utc)
    expiration = issued + TOKEN_DURATION
    payload = {
        "sub": factory.make_UUID(),
        "iss": msm_site,
        "iat": issued.timestamp(),
        "exp": expiration.timestamp(),
        "aud": AUDIENCE,
        # private claims
        "purpose": ENROLMENT,
        "enrolment-url": enrol_url,
    }
    yield payload


@pytest.fixture
def jwt_key(factory):
    key = factory.make_bytes(32)
    yield key


@pytest.fixture
def msm_access(factory, maasdb, msm_site, jwt_key):
    issued = datetime.now(timezone.utc)
    expiration = issued + TOKEN_DURATION
    payload = {
        "sub": factory.make_UUID(),
        "iss": msm_site,
        "iat": issued.timestamp(),
        "exp": expiration.timestamp(),
        "aud": AUDIENCE,
        # private claims
        "purpose": ACCESS,
    }
    secret = {
        "url": urlparse(msm_site)._replace(path="/site/v1/details").geturl(),
        "jwt": jwt.encode(payload, jwt_key, algorithm=TOKEN_ALGORITHM),
    }

    SecretManager().set_composite_secret("msm-connector", secret)
    yield secret


@pytest.mark.usefixtures("maasdb")
class TestMSMEnrol:
    def test_enroll(self, mocker, maas_site, msm_enrol_payload, jwt_key):
        mocked_start_workflow = mocker.patch("maasserver.msm.start_workflow")
        encoded = jwt.encode(
            msm_enrol_payload, jwt_key, algorithm=TOKEN_ALGORITHM
        )
        msm_enrol(encoded)
        mocked_start_workflow.assert_called_once()
        args = mocked_start_workflow.call_args.args
        assert args[0] == "msm-enrol-site"
        assert args[2].site_name == maas_site["maas_name"]
        assert args[2].url == msm_enrol_payload["enrolment-url"]

    def test_bad_jwt(self, mocker, msm_enrol_payload, jwt_key):
        mocker.patch("maasserver.msm.start_workflow")
        bad_payload = dict(msm_enrol_payload, aud="bad-audience")
        encoded = jwt.encode(bad_payload, jwt_key, algorithm=TOKEN_ALGORITHM)
        with pytest.raises(MSMException):
            msm_enrol(encoded)

    def test_missing_url(self, mocker, msm_enrol_payload, jwt_key):
        mocker.patch("maasserver.msm.start_workflow")
        bad_payload = msm_enrol_payload.copy()
        bad_payload.pop("enrolment-url")
        encoded = jwt.encode(bad_payload, jwt_key, algorithm=TOKEN_ALGORITHM)
        with pytest.raises(MSMException):
            msm_enrol(encoded)


@pytest.mark.usefixtures("maasdb")
class TestMSMStatus:
    def test_not_enroled(self, mocker):
        mocked_query = mocker.patch("maasserver.msm._query_workflow")
        mocked_query.return_value = False, None
        st = msm_status()
        mocked_query.assert_not_called()
        assert "sm-url" not in st
        assert "running" not in st

    def test_enroled_not_connected(self, mocker, msm_access):
        mocked_query = mocker.patch("maasserver.msm._query_workflow")
        mocked_query.return_value = False, None
        st = msm_status()
        mocked_query.assert_called_once()
        assert "sm-url" in st
        assert not st["running"]

    def test_enroled_connected(self, mocker, msm_access):
        mocked_query = mocker.patch("maasserver.msm._query_workflow")
        mocked_query.return_value = True, datetime.now()
        st = msm_status()
        mocked_query.assert_called_once()
        assert "sm-url" in st
        assert st["running"]
