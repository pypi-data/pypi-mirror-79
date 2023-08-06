from flask.helpers import url_for


def dynamic_url_for(endpoint, **values):
    rv = url_for(endpoint=endpoint, **values)
    from flask import current_app as app
    if app.config["shouldUseCloudDist"] is True:
        rv = f"{app.config['bucketUrl']}/{app.config['bucketDirPath']}{rv}"
    return rv
