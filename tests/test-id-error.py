import pytest

from api_client.digital_twin import get_device_by_id


def test_get_device_by_id_lanza_error_si_no_hay_id():
    with pytest.raises(ValueError, match="El ID es obligatorio"):
        get_device_by_id("")