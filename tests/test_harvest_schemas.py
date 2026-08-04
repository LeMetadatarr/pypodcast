"""Row-schema equivalence tests for the 2 podcast scrapers.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch2.py / test_scrapers_batch3.py, keeping only the tests
for scrapers that live in this package, re-pointed at pypodcast.harvest.*.
These lock the exact flat-row shape each scraper emits (the contract the
LeData datasets depend on) against a realistic upstream sample, so a future
engine change can't silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pypodcast.harvest.listennotes_podcasts import (
    ListenNotesPodcastsSource,
    _parse_detail,
    _urls_from_listing,
    _ln_id_from_url,
)
from pypodcast.harvest.podcastindex_podcasts import (
    PodcastIndexPodcastsSource,
    map_chart_row,
    map_search_row,
    map_browse_row,
)


# ---------------------------------------------------------------------------
# podcastindex_podcasts  (from test_scrapers_batch2.py)
# ---------------------------------------------------------------------------

def test_podcastindex_map_chart_row():
    entry = {
        "id": {"attributes": {"im:id": "123"}},
        "im:name": {"label": "The Daily"},
        "im:artist": {"label": "NYT"},
        "im:image": [{"label": "img1"}, {"label": "img2"}],
        "link": {"attributes": {"href": "https://example.com/podcast"}},
    }
    row = map_chart_row(entry, "us", "News")
    assert row["itunes_id"] == "123"
    assert row["title"] == "The Daily"
    assert row["image"] == "img2"
    assert row["country_charts"] == ["us"]
    assert row["source"] == "itunes_rss"
    assert set(row) == {
        "itunes_id", "title", "author", "image", "genres", "url",
        "description", "language", "episode_count", "explicit", "feed_url",
        "country_charts", "source", "entity_type",
    }


def test_podcastindex_map_search_row():
    e = {
        "collectionId": 456,
        "collectionName": "Serial",
        "artistName": "This American Life",
        "artworkUrl600": "img600",
        "genres": ["True Crime"],
        "collectionViewUrl": "https://example.com/serial",
        "trackCount": 12,
        "contentAdvisoryRating": "Explicit",
        "feedUrl": "https://example.com/feed.xml",
    }
    row = map_search_row(e)
    assert row["itunes_id"] == "456"
    assert row["explicit"] is True
    assert row["source"] == "itunes_search"


def test_podcastindex_map_row_drops_without_id():
    assert map_chart_row({"id": {}}, "us", "News") is None
    assert map_search_row({}) is None
    assert map_browse_row({"id": {}}, "us", "News") is None


def test_podcastindex_fetch_charts_step_advances_genre_then_country():
    src = PodcastIndexPodcastsSource()
    src.get_json = None
    src._get = lambda url: {"feed": {"entry": []}}
    rows, cursor = src.fetch({"stage": "charts", "cidx": 0, "gidx": 0})
    assert cursor["stage"] == "charts"
    assert cursor["cidx"] == 0
    assert cursor["gidx"] == 1


def test_podcastindex_registered():
    assert all_sources().get("podcastindex_podcasts") is PodcastIndexPodcastsSource


# ---------------------------------------------------------------------------
# listennotes_podcasts  (from test_scrapers_batch3.py)
# ---------------------------------------------------------------------------

def test_listennotes_parse_detail_extracts_jsonld():
    html = (
        '<script type="application/ld+json">'
        '{"@type": "PodcastSeries", "name": "The Daily", "description": "News podcast",'
        ' "image": {"url": "http://img"}, "author": {"name": "NYT"}, "inLanguage": "en",'
        ' "url": "http://site", "genre": ["News"]}'
        '</script>'
    )
    row = _parse_detail(html, "https://www.listennotes.com/podcasts/the-daily-abc123def4/")
    assert row["ln_id"] == "daily-abc123def4"
    assert row["title"] == "The Daily"
    assert row["author"] == "NYT"
    assert row["genres"] == ["News"]
    assert row["entity_type"] == "podcast"
    assert set(row) == {
        "ln_id", "ln_url", "title", "author", "description", "image", "language",
        "genres", "episode_count", "listen_score", "global_rank", "website", "entity_type",
    }


def test_listennotes_parse_detail_drops_without_title():
    assert _parse_detail("<html></html>", "https://www.listennotes.com/podcasts/x-abc123def4/") is None


def test_listennotes_urls_from_listing_itemlist():
    html = (
        '<script type="application/ld+json">'
        '{"@type": "ItemList", "itemListElement": ['
        '{"url": "https://www.listennotes.com/podcasts/a-abc123def4/"},'
        '{"url": "https://www.listennotes.com/podcasts/b-xyz987wvu6/"}]}'
        '</script>'
    )
    urls = _urls_from_listing(html)
    assert len(urls) == 2


def test_listennotes_fetch_listing_stage_advances_and_stops_short():
    src = ListenNotesPodcastsSource()
    src._session = object()
    src.throttle.wait = lambda: None

    class FakeResp:
        status_code = 200

        def raise_for_status(self):
            pass

        text = (
            '<script type="application/ld+json">{"@type": "ItemList", "itemListElement": []}</script>'
        )

    src._get = lambda url: FakeResp()
    src._process_urls = lambda urls: []
    rows, cursor = src.fetch({"stage": "listing", "listing_page": 1, "search_idx": 0, "search_page": 1})
    assert rows == []
    assert cursor["stage"] == "search"


def test_listennotes_registered():
    assert all_sources().get("listennotes_podcasts") is ListenNotesPodcastsSource


def test_pypodcast_scrapers_are_registered():
    reg = all_sources()
    assert reg.get("listennotes_podcasts") is ListenNotesPodcastsSource
    assert reg.get("podcastindex_podcasts") is PodcastIndexPodcastsSource
