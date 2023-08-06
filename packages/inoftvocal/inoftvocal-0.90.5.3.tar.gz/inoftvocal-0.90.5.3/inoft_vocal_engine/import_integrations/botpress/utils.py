def botpress_date_to_timestamp(date_string: str) -> int:
    from datetime import datetime
    return round(datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())
