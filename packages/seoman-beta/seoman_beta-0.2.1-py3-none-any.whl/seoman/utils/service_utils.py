from typing import Dict, Any, List

from .date_utils import create_date_range

from google.auth.exceptions import RefreshError

from .. import auth
from datetime import datetime, timedelta


def create_body_list(
    body: Dict[Any, Any],
    new_body: List[Dict[Any, Any]] = [],
    detail_level: int = 1,
) -> List[Dict[Any, Any]]:
    """
    Gets a body, and creates a new body from that.
    """

    dates = create_date_range(
        start=body.get("startDate"), end=body.get("endDate"), day_interval=detail_level
    )

    if detail_level != 1:
        for idx in range(len(dates)):
            try:
                """
                If the detail level is low, medium or high
                reduce end day by one to prevent duplications.
                """
                body.update(
                    {
                        "startDate": dates[idx],
                        "endDate": (
                            datetime.strptime(dates[idx + 1], "%Y-%m-%d")
                            - timedelta(days=1)
                        ).strftime("%Y-%m-%d"),
                    }
                )
                new_body.append(body.copy())
            except IndexError:
                pass
    else:
        for date in dates:
            body.update({"startDate": date, "endDate": date})
            new_body.append(body.copy())

    return new_body


def path_exists(filename: str) -> bool:
    """
    Checks for the given file path exists.
    """
    from pathlib import Path

    return Path(filename).exists()


def regenerate_credentials(method):
    """
    If query raises RefreshError(Expired token causes this.)
    It automatically regenerate credentials
    and runs the method again.
    """

    def run_query(*args, **kw):
        try:
            result = method(*args, **kw)
        except RefreshError:
            auth.get_authenticated()
            auth.load_service()
            result = method(*args, **kw)

        return result

    return run_query
