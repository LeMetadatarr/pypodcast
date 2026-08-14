# Dataset

## What this repo produces

`pypodcast` provides two podcast catalog harvesters:

- `listennotes_podcasts` scrapes podcast pages from ListenNotes, including curated lists and keyword search results.
- `podcastindex_podcasts` sweeps Apple/iTunes podcast sources: top-podcasts charts by country and genre, search results, and genre browse lists.

Each harvester writes one JSONL file where each row is a distinct podcast show.

## Dataset format

### `listennotes_podcasts`

One row per podcast show. Each row is a JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `ln_id` | string | ListenNotes podcast identifier. |
| `ln_url` | string | ListenNotes podcast page URL. |
| `title` | string | Podcast title. |
| `author` | string or null | Podcast author or publisher. |
| `description` | string or null | Short description, up to 600 characters. |
| `image` | string or null | Cover image URL. |
| `language` | string or null | Language code when available. |
| `genres` | list of strings | Genre labels from JSON-LD. |
| `episode_count` | integer or null | Number of episodes when shown. |
| `listen_score` | integer or null | ListenScore when shown. |
| `global_rank` | string or null | Global rank string when shown. |
| `website` | string or null | Podcast website URL. |
| `entity_type` | string | Always `"podcast"`. |

### `podcastindex_podcasts`

One row per podcast show. Each row is a JSON object with these fields:

| Field | Type | Description |
| --- | --- | --- |
| `itunes_id` | string | iTunes collection identifier. |
| `title` | string or null | Podcast title. |
| `author` | string or null | Artist or publisher name. |
| `image` | string or null | Artwork URL. |
| `genres` | list of strings | Genre names or IDs. |
| `url` | string or null | iTunes collection URL. |
| `description` | string or null | Description when available. |
| `language` | string or null | Language code when available. |
| `episode_count` | integer or null | Track count from search results. |
| `explicit` | boolean or null | Explicit flag from search results. |
| `feed_url` | string or null | RSS feed URL from search results. |
| `country_charts` | list of strings | Countries where the podcast appeared in charts. |
| `source` | string | One of `itunes_rss`, `itunes_search`, or `apple_browse`. |
| `entity_type` | string | Always `"podcast"`. |

## How to generate it

Install the package and run either harvester:

```bash
pip install pypodcast

pypodcast-harvest listennotes_podcasts \
  --output ~/.cache/metadatarr/scrapers/

pypodcast-harvest podcastindex_podcasts \
  --output ~/.cache/metadatarr/scrapers/
```

Both harvests are resumable. You can stop either with Ctrl-C and rerun the same command to continue from the last checkpoint.

## Worth publishing on Hugging Face?

Yes. Aggregated podcast metadata is scarce and the dataset contains only public show-level information. It supports recommendation and search research and does not include episode audio or transcripts.

## ML tasks served

- Podcast recommendation and search ranking.
- Genre and language classification.
- RSS feed discovery.
- Named entity recognition on titles and descriptions.
- Cross-catalog entity linking.
