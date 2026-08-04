# pypodcast

2 podcast catalog bulk harvesters grouped onto the
[harvestkit](https://github.com/LeMetadatarr/harvestkit) resumable-harvest
engine. Extracted from [metadatarr](https://github.com/TigreGotico/metadatarr)'s
scraper collection into its own standalone package.

## Sources

| Scraper | Registry name | Source |
| --- | --- | --- |
| `listennotes_podcasts` | `listennotes_podcasts` | ListenNotes (HTML scrape, no API key) |
| `podcastindex_podcasts` | `podcastindex_podcasts` | Apple/iTunes charts + search + browse (no auth) |

## Install

```bash
pip install pypodcast
# or, for the HuggingFace publisher (via harvestkit):
pip install "pypodcast[hf]"
# or, for Cloudflare-guarded sources:
pip install "pypodcast[stealth]"
```

## Usage

```bash
# list every registered scraper
pypodcast-harvest --list

# harvest one source (resumable — safe to Ctrl-C and rerun)
pypodcast-harvest listennotes_podcasts --output ~/.cache/metadatarr/scrapers/
```

Every scraper is a `harvestkit.engine.Source` subclass: checkpoint/dedup/
pagination/throttle are handled by the shared engine, each module only
answers `initial_cursor()` and `fetch(cursor)`. See
[harvestkit](https://github.com/LeMetadatarr/harvestkit) for the full engine
API.

## License

Apache-2.0
