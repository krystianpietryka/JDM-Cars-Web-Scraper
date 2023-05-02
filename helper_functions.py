def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = round((seconds % 60) ,2)
    if hours == 0:
        if minutes == 0:
            return f"{seconds}s"
        else:
            return f"{minutes}m {seconds}s"
        pass
    return f"{hours}h {minutes}m {seconds}s"


def make_hyperlink(value):
    url = "https:/{}"
    return '=HYPERLINK("%s", "%s")' % (url.format(value), value)
