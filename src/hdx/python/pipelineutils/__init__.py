import re
from datetime import datetime

from hdx.data.dataset import Dataset

template = re.compile("{{.*?}}")


def string_params_to_dict(string: str) -> dict[str, str]:
    params = {}
    if not string:
        return params
    for name_par in string.split(","):
        name, par = name_par.strip().split(":")
        params[name] = par.strip()
    return params


def match_template(input: str) -> tuple[str | None, str | None]:
    """Try to match {{XXX}} in input string

    Args:
        input: String in which to look for template

    Returns:
        (Matched string with brackets, matched string without brackets)
    """
    match = template.search(input)
    if match:
        template_string = match.group()
        return template_string, template_string[2:-2]
    return None, None


def get_startend_dates_from_time_period(
    dataset: Dataset, today: datetime | None = None
) -> dict | None:
    """Return the time period in form required for source_date

    Args:
        dataset: Dataset object
        today: Date to use for today. Default is None (datetime.utcnow)

    Returns:
        Time period in form required for source_date
    """
    if today is None:
        date_info = dataset.get_time_period()
    else:
        date_info = dataset.get_time_period(today=today)
    startdate = date_info.get("startdate")
    enddate = date_info.get("enddate")
    if enddate is None:
        return None
    return {"start": startdate, "end": enddate}
