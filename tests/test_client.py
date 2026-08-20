"""Unit tests for MatomoClient (HTTP is mocked with unittest.mock)."""

from unittest import mock

import pytest

from matomopy import (
    MatomoAPIError,
    MatomoAuthenticationError,
    MatomoClient,
    MatomoConfigError,
    MatomoHTTPError,
)


def make_response(json_data=None, status=200, text="", content=b""):
    response = mock.Mock()
    response.status_code = status
    response.text = text
    response.content = content
    if json_data is None:
        response.json.side_effect = ValueError("no json")
    else:
        response.json.return_value = json_data
    return response


def make_client(response, **kwargs):
    session = mock.Mock()
    session.post.return_value = response
    session.get.return_value = response
    return (
        MatomoClient(
            "https://analytics.example.org",
            token_auth="TOKEN",
            session=session,
            **kwargs,
        ),
        session,
    )


def test_endpoint_normalization():
    variants = [
        "https://a.example.org",
        "https://a.example.org/",
        "https://a.example.org/index.php",
    ]
    for base in variants:
        client = MatomoClient(base, session=mock.Mock())
        assert client.endpoint.endswith("index.php")


def test_empty_base_url_rejected():
    with pytest.raises(MatomoConfigError):
        MatomoClient("", session=mock.Mock())


def test_call_posts_expected_parameters():
    response = make_response(json_data={"nb_visits": 5})
    client, session = make_client(response)

    result = client.call("VisitsSummary.get", id_site=1, period="day", date="today")

    assert result == {"nb_visits": 5}
    _, kwargs = session.post.call_args
    assert kwargs["params"] == {"module": "API"}
    sent = dict(kwargs["data"])
    assert sent["method"] == "VisitsSummary.get"
    assert sent["idSite"] == "1"
    assert sent["period"] == "day"
    assert sent["date"] == "today"
    assert sent["format"] == "json"
    assert sent["token_auth"] == "TOKEN"


def test_default_id_site_is_used():
    response = make_response(json_data={})
    client, session = make_client(response, default_id_site=7)
    client.call("VisitsSummary.get", period="day", date="today")
    sent = dict(session.post.call_args.kwargs["data"])
    assert sent["idSite"] == "7"


def test_per_call_token_auth_overrides_the_client_token():
    response = make_response(json_data={})
    client, session = make_client(response)
    client.call("VisitsSummary.get", token_auth="PER_CALL_TOKEN")
    sent = dict(session.post.call_args.kwargs["data"])
    assert sent["token_auth"] == "PER_CALL_TOKEN"


def test_bearer_auth_sets_header_and_not_body():
    response = make_response(json_data={})
    client, session = make_client(response, auth_method="bearer")
    client.call("API.getMatomoVersion")
    kwargs = session.post.call_args.kwargs
    assert kwargs["headers"]["Authorization"] == "Bearer TOKEN"
    assert "token_auth" not in dict(kwargs["data"])


def test_api_error_is_raised():
    response = make_response(json_data={"result": "error", "message": "Report not found"})
    client, _ = make_client(response)
    with pytest.raises(MatomoAPIError) as exc:
        client.call("Bad.method")
    assert "Report not found" in str(exc.value)


def test_authentication_error_is_detected():
    response = make_response(
        json_data={
            "result": "error",
            "message": "You must provide a token_auth.",
        }
    )
    client, _ = make_client(response)
    with pytest.raises(MatomoAuthenticationError):
        client.call("VisitsSummary.get", id_site=1)


def test_http_error_is_raised():
    response = make_response(status=500, text="boom")
    client, _ = make_client(response)
    with pytest.raises(MatomoHTTPError) as exc:
        client.call("VisitsSummary.get", id_site=1)
    assert exc.value.status_code == 500


def test_non_json_format_returns_text():
    response = make_response(text="a;b;c", status=200)
    client, _ = make_client(response)
    result = client.call("VisitsSummary.get", id_site=1, format="csv")
    assert result == "a;b;c"


def test_raw_returns_bytes():
    response = make_response(content=b"\x89PNG", status=200)
    client, _ = make_client(response)
    result = client.call("ImageGraph.get", id_site=1, raw=True)
    assert result == b"\x89PNG"


def test_module_proxy_dispatches_to_call():
    response = make_response(json_data={"nb_visits": 3})
    client, session = make_client(response)
    result = client.VisitsSummary.get(id_site=1, period="day", date="today")
    assert result == {"nb_visits": 3}
    sent = dict(session.post.call_args.kwargs["data"])
    assert sent["method"] == "VisitsSummary.get"


def test_private_attribute_access_raises():
    client, _ = make_client(make_response(json_data={}))
    with pytest.raises(AttributeError):
        _ = client._not_a_module


def test_paginate_walks_pages():
    session = mock.Mock()
    page1 = make_response(json_data=[{"n": 1}, {"n": 2}])
    page2 = make_response(json_data=[{"n": 3}])
    session.post.side_effect = [page1, page2]
    client = MatomoClient("https://a.example.org", session=session, max_retries=0)
    rows = list(client.paginate("Actions.getPageUrls", id_site=1, page_size=2))
    assert [r["n"] for r in rows] == [1, 2, 3]


def test_paginate_rejects_conflicting_filter_params():
    client, _ = make_client(make_response(json_data=[]))
    with pytest.raises(MatomoConfigError):
        list(client.paginate("Actions.getPageUrls", id_site=1, filter_limit=10))


def test_supplied_session_adapters_are_left_alone():
    session = mock.Mock()
    MatomoClient("https://a.example.org", session=session, max_retries=3)
    session.mount.assert_not_called()


def test_bulk_request_builds_indexed_urls():
    response = make_response(json_data=[{}, {}])
    client, session = make_client(response)
    client.bulk_request(
        [
            "method=VisitsSummary.get&idSite=1&period=day&date=today",
            {"method": "Actions.get", "idSite": 1},
        ]
    )
    sent = dict(session.post.call_args.kwargs["data"])
    assert sent["method"] == "API.getBulkRequest"
    assert "urls[0]" in sent
    assert "urls[1]" in sent
