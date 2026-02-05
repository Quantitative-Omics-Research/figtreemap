import importlib
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from lxml import etree


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


class FakeResponse:
    def __init__(self, json_data=None, content=b""):
        self._json = json_data or {}
        self.content = content

    def json(self):
        return self._json

    def raise_for_status(self):
        pass


def import_module_with_build():
    """
    Prevent real HTTP call during module import by mocking
    get_phylopics_build_number's underlying request.
    """
    with patch("requests.get") as mock_get:
        mock_get.return_value = FakeResponse({"build": 123})
        import figtreemap.phylopics as mod

        importlib.reload(mod)
    return mod


# ---------------------------------------------------------------------
# get_phylopics_build_number
# ---------------------------------------------------------------------


def test_get_phylopics_build_number_returns_build():
    mod = import_module_with_build()

    with patch("requests.get") as mock_get:
        mock_get.return_value = FakeResponse({"build": 999})

        build = mod.get_phylopics_build_number()

    assert build == 999


# ---------------------------------------------------------------------
# get_lineage_ott_ids
# ---------------------------------------------------------------------


def test_get_lineage_ott_ids_extracts_ids():
    mod = import_module_with_build()

    fake_record = MagicMock()
    fake_record.response_dict = {
        "lineage": [
            {"ott_id": 10},
            {"ott_id": 20},
            {"ott_id": 30},
        ]
    }

    with patch.object(mod.OT, "taxon_info", return_value=fake_record):
        result = mod.get_lineage_ott_ids(123)

    assert result == [10, 20, 30]


# ---------------------------------------------------------------------
# get_phylopic_svg_url_from_ott_ids
# ---------------------------------------------------------------------


def test_get_phylopic_svg_url_from_ott_ids_returns_vector_href():
    mod = import_module_with_build()
    mod.build = 555  # avoid using import-time value

    first = FakeResponse({"_links": {"primaryImage": {"href": "/img/abc"}}})

    second = FakeResponse(
        {"_links": {"vectorFile": {"href": "https://cdn.test/file.svg"}}}
    )

    with (
        patch.object(mod, "get_build", return_value=555),
        patch("requests.get", side_effect=[first, second]) as mock_get,
    ):
        url = mod.get_phylopic_svg_url_from_ott_ids([1, 2, 3])

    assert url == "https://cdn.test/file.svg"

    # confirm first request contained ott ids + build
    first_call_url = mock_get.call_args_list[0].args[0]
    assert "objectIDs=1,2,3" in first_call_url
    assert "build=555" in first_call_url


# ---------------------------------------------------------------------
# get_svg (full integration, mocked)
#
