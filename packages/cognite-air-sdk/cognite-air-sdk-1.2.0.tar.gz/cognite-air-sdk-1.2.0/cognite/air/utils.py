import json
from typing import Union


def valfilter(cond, dct):
    """Filters items in dictionary by cond(value)"""
    return {k: v for k, v in dct.items() if cond(v)}


def is_jsonable(data: Union[str, bytes, bytearray]) -> bool:
    try:
        json.loads(data)
        return True
    except Exception:
        return False


def strip_patch_from_version(version: str) -> str:
    if not isinstance(version, str):
        raise TypeError(f"Expected input '{version}' to be of type {str}, not {type(version)}")

    if version.count(".") > 2:
        raise ValueError("Expected at most two dots in version string, e.g. '1.33.7'")

    return ".".join(version.split(".")[:2])


def is_string_truthy(bool_like):
    """
    This function tries to solve the annoying problem of checking whether a given
    string is thruthy or not. It also accepts booleans and None.

    String caPitaLizaTIon is ignored.
    """
    if bool_like is None:
        return False

    elif isinstance(bool_like, bool):
        return bool_like

    elif not isinstance(bool_like, str):
        raise TypeError(f"Expected one of {[bool, str, None]}, got {type(bool_like)}")

    return bool_like.capitalize() == "True"
