"""pypodcast — podcast catalog bulk harvesters, grouped on harvestkit.

Importing this package imports :mod:`pypodcast.harvest`, which in turn
imports every scraper module so it registers itself with
:mod:`harvestkit.engine` (``@register``).
"""
from pypodcast.version import __version__

import pypodcast.harvest  # noqa: F401  (import for @register side effects)

__all__ = ["__version__"]
