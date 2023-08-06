from typing import Dict, Any, List

from .date_utils import create_date_range

from google.auth.exceptions import RefreshError


def create_body_list(
    body: Dict[Any, Any], new_body: List[Dict[Any, Any]] = []
) -> List[Dict[Any, Any]]:
    """
    Gets a body, and creates a new body from that.
    """

    dates = create_date_range(start=body.get("startDate"), end=body.get("endDate"))

    for date in dates:
        body.update({"startDate": date, "endDate": date})
        new_body.append(body.copy())

    return new_body


def path_exists(filename: str) -> bool:

    from pathlib import Path

    return Path(filename).exists()


def regenerate_credentials(method):
    def try_catch(*args, **kw):
        try:
            result = method(*args, **kw)
        except RefreshError:
            get_authenticated()
            load_service()
            result = method(*args, **kw)

        return result

    return try_catch

