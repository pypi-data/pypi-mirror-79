from flask import Blueprint, render_template, request, Response, jsonify, redirect
from typing import List

from inoft_vocal_engine.cloud_ressources.account_resources import AccountResources
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.web_interface.auth.models import AccountData

auth_blueprint = Blueprint("auth", __name__, template_folder="templates")

@auth_blueprint.route('/login')
def login():
    engine_resources = EngineResources()
    account_resources = AccountResources(engine_resources=engine_resources)

    login_success = account_resources.login_with_cookies(cookies=request.cookies)
    if login_success is not True:
        return render_template("auth/login.html")
    else:
        return redirect(f"{account_resources.account_username}/control-panel")

@auth_blueprint.route('/auth_backend/login', methods=["POST"])
def auth_backend_login():
    engine_resources = EngineResources()
    account_resources = AccountResources(engine_resources=engine_resources)

    data = SafeDict(request.get_json())
    username_or_email = data.get("usernameOrEmail").to_str(default=None)
    encrypted_password = data.get("encryptedPassword").to_str(default=None)

    if username_or_email is not None and encrypted_password is not None:
        account_has_been_found, account_has_been_logged_in, new_auth_token_value = account_resources.login(
            username_or_email=username_or_email, encrypted_password=encrypted_password
        )

        if account_has_been_logged_in is True:
            print(new_auth_token_value)
            return jsonify({
                "loginSuccess": True,
                "accountUsername": account_resources.account_username,
                "accountId": account_resources.account_id,
                "newAuthToken": new_auth_token_value
            })
        else:
            return jsonify({
                "loginSuccess": False
            })
    else:
        # todo: change that to have the same format everywhere
        if username_or_email is None and encrypted_password is None:
            return Response("mailAndPasswordFieldsEmpty", status=401)
        elif username_or_email is None:
            return Response("mailFieldEmpty", status=401)
        elif username_or_email is None:
            return Response("passwordFieldEmpty", status=401)

@auth_blueprint.route('/auth_backend/login-with-amazon', methods=["POST"])
def login_with_amazon():
    authorization_code = SafeDict(request.get_json()).get("authorizationCode").to_str(default=None)
    if authorization_code is not None:
        from inoft_vocal_engine.web_interface.auth.login_with_amazon import LoginWithAmazon
        tokens = LoginWithAmazon().authorization_code_to_tokens(authorization_code=authorization_code)

        from inoft_vocal_engine.smapi_clients.smapi_base_client import SmapiBaseClient
        smapi_client = SmapiBaseClient(refresh_token=tokens.refresh_token)
        skills_summaries = smapi_client.get_list_skills_of_account()

        skills_dicts: List[dict] = list()
        for skill in skills_summaries:
            skills_dicts.append(skill.to_dict())

        print(skills_dicts)

        smapi_client.create_skill(vendor_id=smapi_client.get_vendors_of_account()[0].id)

        return jsonify(success=True, skills=skills_dicts)
    return jsonify(success=False)


