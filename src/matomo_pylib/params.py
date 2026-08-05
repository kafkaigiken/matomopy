"""Helpers for turning Python values into Matomo HTTP parameters.

Matomo's HTTP API accepts scalar query parameters, comma-separated lists
(e.g. ``idSites=1,2,3`` or ``columns=nb_visits,nb_actions``), and
PHP-style bracketed arrays for structured values (e.g.
``urls[0]=...&urls[1]=...``). This module normalises ordinary Python
values (``bool``, ``list``, ``dict``, ``None``) into the shapes Matomo
expects.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from urllib.parse import urlencode

# Parameter aliases: friendly Pythonic names -> the exact Matomo name.
# Only a handful of Matomo parameters use camelCase; the rest already use
# snake_case (``filter_limit`` etc.), so we translate just the common ones.
PARAM_ALIASES: Dict[str, str] = {
    "id_site": "idSite",
    "id_sites": "idSites",
    "id_goal": "idGoal",
    "id_subtable": "idSubtable",
    "id_dimension": "idDimension",
    "id_report": "idReport",
}

# isinstance() targets used in the per-parameter encoding path, hoisted to
# module level so the type-tuples are built once rather than on every value.
_SEQUENCE_TYPES = (list, tuple)
_CONTAINER_TYPES = (list, tuple, dict)


def normalize_bool(value: bool) -> str:
    """Return Matomo's textual representation of a boolean (``1``/``0``)."""
    return "1" if value else "0"


def _encode(key: str, value: Any, out: List[Tuple[str, str]]) -> None:
    """Recursively encode ``value`` under ``key`` into ``out``.

    * ``None`` is skipped entirely (the parameter is omitted).
    * ``bool`` becomes ``"1"``/``"0"``.
    * ``list``/``tuple`` of scalars becomes a comma-separated string.
    * ``dict`` (or a list containing dicts/lists) becomes bracketed keys,
      e.g. ``key[a]=1`` or ``key[0][b]=2``.
    * everything else is stringified.
    """
    if value is None:
        return

    if isinstance(value, bool):
        out.append((key, normalize_bool(value)))
        return

    if isinstance(value, dict):
        for sub_key, sub_value in value.items():
            _encode(f"{key}[{sub_key}]", sub_value, out)
        return

    if isinstance(value, _SEQUENCE_TYPES):
        if not value:
            # An empty sequence means "no value"; sending ``key=`` would make
            # Matomo apply an empty filter instead of omitting it.
            return

        # A flat list of scalars is best expressed as a comma-joined
        # string, which is what the vast majority of Matomo list
        # parameters expect (idSites, columns, hideColumns, ...).
        if all(not isinstance(item, _CONTAINER_TYPES) for item in value):
            joined = ",".join(
                normalize_bool(item) if isinstance(item, bool) else str(item) for item in value if item is not None
            )
            out.append((key, joined))
        else:
            # Nested structures need PHP-style indexed brackets.
            for index, item in enumerate(value):
                _encode(f"{key}[{index}]", item, out)
        return

    out.append((key, str(value)))


def encode_params(params: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Flatten a parameter mapping into a list of ``(name, value)`` pairs.

    ``None`` values are dropped so callers can pass optional parameters
    unconditionally. Aliases in :data:`PARAM_ALIASES` are translated to
    their Matomo names.

    Args:
        params: Raw parameter mapping (Pythonic or Matomo names).

    Returns:
        A list of string ``(name, value)`` tuples ready to hand to
        ``requests`` as ``params`` or ``data``.
    """
    out: List[Tuple[str, str]] = []
    for key, value in params.items():
        matomo_key = PARAM_ALIASES.get(key, key)
        _encode(matomo_key, value, out)
    return out


def encode_query(params: Dict[str, Any]) -> str:
    """Encode ``params`` into a URL query string using Matomo's conventions.

    Combines :func:`encode_params` with :func:`urllib.parse.urlencode`; used
    for building the sub-requests of a bulk API call and the queued entries of
    the bulk tracker.
    """
    return urlencode(encode_params(params))
