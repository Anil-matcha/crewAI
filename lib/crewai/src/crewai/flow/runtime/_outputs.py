"""Shared FlowDefinition runtime output helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from crewai.utilities.serialization import to_serializable


def outputs_by_name(
    method_outputs: list[Any],
    *,
    local_outputs: Mapping[str, Any] | None = None,
    serialize: bool = False,
) -> dict[str, Any]:
    outputs: dict[str, Any] = {}
    for entry in method_outputs:
        method = ""
        output = entry
        if isinstance(entry, dict) and "output" in entry:
            method = str(entry.get("method", ""))
            output = entry["output"]
        outputs[method] = _output_value(output, serialize=serialize)

    if local_outputs is not None:
        if not isinstance(local_outputs, Mapping):
            raise TypeError("flow definition local outputs must be a mapping")
        outputs.update(
            {
                key: _output_value(output, serialize=serialize)
                for key, output in local_outputs.items()
            }
        )

    return outputs


def _output_value(value: Any, *, serialize: bool) -> Any:
    if not serialize:
        return value
    return to_serializable(value, max_depth=0)
