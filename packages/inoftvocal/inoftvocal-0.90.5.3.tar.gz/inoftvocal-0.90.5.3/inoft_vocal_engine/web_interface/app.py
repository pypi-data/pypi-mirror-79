from flask import Flask, Response, render_template, request

from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.route_blueprints.auth import auth_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.audio_editor import audio_editor_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.code_editor import code_editor_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.contents import contents_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.control_panel import control_panel_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.deployment.deployment import deployment_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.diagrams import diagrams_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.intents import intents_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.dynamic_url_for import dynamic_url_for
from inoft_vocal_engine.web_interface.route_blueprints.permissions import permissions_blueprint
from inoft_vocal_engine.web_interface.route_blueprints.team_organization import organization_blueprint

def strip_spaces(string: str):
    return string.strip()

app = Flask(__name__)
app.config["shouldUseCloudDist"] = False
app.config["bucketUrl"] = "https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com"
app.config["bucketDirPath"] = "prod"
app.jinja_env.globals.update(url_for=dynamic_url_for)
# app.config['SERVER_NAME'] = 'example.com'
app.jinja_env.filters["strip_spaces"] = strip_spaces

app.register_blueprint(control_panel_blueprint)
app.register_blueprint(contents_blueprint)
app.register_blueprint(audio_editor_blueprint)
app.register_blueprint(organization_blueprint)
app.register_blueprint(diagrams_blueprint)
app.register_blueprint(intents_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(code_editor_blueprint)
app.register_blueprint(permissions_blueprint)
app.register_blueprint(deployment_blueprint)


@app.route("/")
def index():
    from inoft_vocal_engine.web_interface.route_blueprints.contents import contents
    return contents("anvers1944")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/text")
def text():
    return render_template("text-editor/test.html")

@app.route("/equalizer")
def equalizer():
    return render_template("equalizer/index.html")

@app.route("/project_dir", methods=["POST"])
def change_project_dir():
    data = SafeDict(request.get_json())
    filepath = data.get("filepath").to_str(default=None)
    # list_content = content_list(filepath=filepath)
    # return jsonify({"html": list_content})

@app.errorhandler(404)
def error_404(error):
    return Response("Erreur 404")

def lambda_handler(event, context):
    import awsgi
    print(f"event :")
    print(event)
    print("context :")
    print(context)
    return awsgi.response(app=app, event=event, context=context)

if __name__ == '__main__':
    # import serverless_wsgi
    # rest_data = {'resource': '/', 'path': '/', 'httpMethod': 'GET', 'headers': None, 'multiValueHeaders': None, 'queryStringParameters': None, 'multiValueQueryStringParameters': None, 'pathParameters': None, 'stageVariables': None, 'requestContext': {'resourceId': 's1dd4la1h9', 'resourcePath': '/', 'httpMethod': 'GET', 'extendedRequestId': 'Qy0WcGnbiGYFZmQ=', 'requestTime': '05/Aug/2020:11:39:59 +0000', 'path': '/', 'accountId': '631258222318', 'protocol': 'HTTP/1.1', 'stage': 'test-invoke-stage', 'domainPrefix': 'testPrefix', 'requestTimeEpoch': 1596627599596, 'requestId': 'a79afdd7-17e7-47e9-820b-cc2990626e6e', 'identity': {'cognitoIdentityPoolId': None, 'cognitoIdentityId': None, 'apiKey': 'test-invoke-api-key', 'principalOrgId': None, 'cognitoAuthenticationType': None, 'userArn': 'arn:aws:iam::631258222318:root', 'apiKeyId': 'test-invoke-api-key-id', 'userAgent': 'aws-internal/3 aws-sdk-java/1.11.820 Linux/4.9.217-0.1.ac.205.84.332.metal1.x86_64 OpenJDK_64-Bit_Server_VM/25.252-b09 java/1.8.0_252 vendor/Oracle_Corporation', 'accountId': '631258222318', 'caller': '631258222318', 'sourceIp': 'test-invoke-source-ip', 'accessKey': 'ASIAZF6PMB3XEKJLVGOT', 'cognitoAuthenticationProvider': None, 'user': '631258222318'}, 'domainName': 'testPrefix.testDomainName', 'apiId': 'bfcq7086f9'}, 'body': None, 'isBase64Encoded': False}
    # print(serverless_wsgi.handle_request(app=app, event=rest_data, context=None))
    app.run()
