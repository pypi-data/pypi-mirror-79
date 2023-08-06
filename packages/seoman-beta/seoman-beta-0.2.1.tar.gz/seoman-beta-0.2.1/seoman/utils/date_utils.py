from datetime import datetime, timedelta
from typing import Optional, Dict, List, Optional


def get_start_date(days: int) -> str:
    return str(datetime.today().date() - timedelta(days=days))


def get_today() -> str:
    return str(datetime.today().date())


def days_last_util(days: int) -> Dict[str, str]:
    startDate = get_start_date(days)
    endDate = get_today()
    return {"startDate": startDate, "endDate": endDate}


def create_date(year: str = None, month: str = None) -> str:
    if year and month:
        return f"{year}-{month}-01"
    if year:
        return f"{year}-01-01"
    if month:
        return f"{datetime.now().year}-{month}-01"
    else:
        return f"{datetime.now().year}-01-01"


# TODO FIX DATE
def create_date_range(
    days: Optional[int] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    day_interval: int = 1,
) -> List[datetime]:

    if start and end:
        new_end, new_start = (
            datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1),
            datetime.strptime(start, "%Y-%m-%d"),
        )

        day_diff = (new_end - new_start).days
        dates = sorted(
            [
                (new_end - timedelta(days=x + 1)).strftime("%Y-%m-%d")
                for x in range(0, abs(day_diff), day_interval)
            ]
        )

        if dates[0] != start:
            dates.insert(0, start)
        if dates[-1] != end:
            dates.append(end)
        return dates

    return sorted(
        [
            (datetime.today().date() - timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range(days)
        ]
    )
