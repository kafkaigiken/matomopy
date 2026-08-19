"""Unit tests for MatomoTracker (HTTP is mocked with unittest.mock)."""

import json
from unittest import mock

import pytest

from matomopy import (
    MatomoConfigError,
    MatomoHTTPError,
    MatomoTracker,
    generate_visitor_id,
)


def make_response(status=200, text="", json_data=None):
    response = mock.Mock()
    response.status_code = status
    response.text = text
    if json_data is None:
        response.json.side_effect = ValueError("no json")
    else:
        response.json.return_value = json_data
    return response


def make_tracker(**kwargs):
    session = mock.Mock()
    session.get.return_value = make_response(status=204)
    session.post.return_value = make_response(status=204)
    tracker = MatomoTracker(
        "https://analytics.example.org",
        id_site=1,
        session=session,
        **kwargs,
    )
    return tracker, session


def sent_params(session):
    # Single tracking requests are sent as a POST with the parameters in the
    # form body (keeps token_auth out of the URL so privileged params like
    # `cip` are honoured).
    return dict(session.post.call_args.kwargs["data"])


def test_endpoint_normalization():
    tracker, _ = make_tracker()
    assert tracker.endpoint.endswith("matomo.php")


def test_generate_visitor_id_length():
    assert len(generate_visitor_id()) == 16


def test_track_page_view_sends_core_params():
    tracker, session = make_tracker()
    tracker.track_page_view("Homepage", url="https://shop.example/")
    params = sent_params(session)
    assert params["idsite"] == "1"
    assert params["rec"] == "1"
    assert params["action_name"] == "Homepage"
    assert params["url"] == "https://shop.example/"


def test_track_event_params():
    tracker, session = make_tracker()
    tracker.track_event("Video", "Play", name="Intro", value=1.0)
    params = sent_params(session)
    assert params["e_c"] == "Video"
    assert params["e_a"] == "Play"
    assert params["e_n"] == "Intro"
    assert params["e_v"] == "1.0"


def test_visitor_and_user_id_persist():
    tracker, session = make_tracker()
    vid = generate_visitor_id()
    tracker.set_visitor_id(vid).set_user_id("user@example.org")
    tracker.track_page_view("Page")
    params = sent_params(session)
    assert params["_id"] == vid
    assert params["uid"] == "user@example.org"


def test_ecommerce_order_encodes_items():
    tracker, session = make_tracker()
    tracker.track_ecommerce_order(
        order_id="A1",
        grand_total=42.0,
        items=[["sku1", "Widget", "Tools", 21.0, 2]],
    )
    params = sent_params(session)
    assert params["idgoal"] == "0"
    assert params["ec_id"] == "A1"
    assert json.loads(params["ec_items"]) == [["sku1", "Widget", "Tools", 21.0, 2]]


def test_custom_dimension_param():
    tracker, session = make_tracker()
    tracker.set_custom_dimension(3, "premium")
    tracker.track_page_view("Page")
    params = sent_params(session)
    assert params["dimension3"] == "premium"


def test_bulk_mode_queues_then_flushes():
    tracker, session = make_tracker(token_auth="TOKEN")
    tracker.enable_bulk_tracking()
    assert tracker.track_page_view("A") is None
    assert tracker.track_page_view("B") is None
    session.get.assert_not_called()

    tracker.flush()
    payload = session.post.call_args.kwargs["json"]
    assert len(payload["requests"]) == 2
    assert payload["token_auth"] == "TOKEN"
    assert tracker._queue == []


def test_force_new_visit_applies_to_next_request_only():
    tracker, session = make_tracker()
    tracker.set_force_new_visit()

    tracker.track_page_view("A")
    assert sent_params(session)["new_visit"] == "1"

    tracker.track_page_view("B")
    assert "new_visit" not in sent_params(session)


def test_track_action_keeps_page_url_and_reports_target():
    tracker, session = make_tracker()
    tracker.set_url("https://shop.example/pricing")
    tracker.track_action("https://cdn.example/report.pdf", action_type="download")
    params = sent_params(session)
    assert params["url"] == "https://shop.example/pricing"
    assert params["download"] == "https://cdn.example/report.pdf"


def test_track_action_falls_back_to_action_url():
    tracker, session = make_tracker()
    tracker.track_action("https://partner.example", action_type="link")
    params = sent_params(session)
    assert params["url"] == "https://partner.example"
    assert params["link"] == "https://partner.example"


def test_failed_flush_keeps_the_queue():
    tracker, session = make_tracker()
    session.post.return_value = make_response(status=500, text="boom")
    tracker.enable_bulk_tracking()
    tracker.track_page_view("A")

    with pytest.raises(MatomoHTTPError):
        tracker.flush()
    assert len(tracker._queue) == 1


def test_non_hex_visitor_id_rejected():
    tracker, _ = make_tracker()
    with pytest.raises(MatomoConfigError):
        tracker.set_visitor_id("z" * 16)
