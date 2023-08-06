from typing import Any, Tuple, Optional, List
from pydantic import validate_arguments
from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.web_interface.auth.models import AccountData


class AccountResources:
    @validate_arguments
    def __init__(self, engine_resources: Any):
        self.engine_resources: EngineResources = engine_resources
        # self.account_username = account_username
        # self._account_id = None
        self.is_logged_in = False
        self.account_id = None
        self.account_username = None

    """
    @property
    def account_id(self) -> str:
        if self._account_id is None:
            account_data, account_been_found = self.engine_resources.accounts_data_dynamodb_client.get_account_by_username(
               username=self.account_username, fields_to_get=["accountId"],
            )
            if account_been_found is True:
                account_data = AccountData(**account_data)
                self._account_id = account_data.accountId
        return self._account_id
    """

    def _is_valid_auth_token_and_remove_old_tokens(self, account_id: str, auth_token: str) -> bool:
        account_data = self.engine_resources.accounts_data_dynamodb_client.remove_old_auth_tokens(
            account_id=account_id, fields_to_get=["accountId", "authTokens", "username"]
        )
        for valid_auth_token_item in account_data.authTokens:
            if auth_token == valid_auth_token_item.token:
                self.is_logged_in = True
                self.account_id = account_data.accountId
                self.account_username = account_data.username
                return True
        return False

    def login(self, username_or_email: str, encrypted_password: str) -> Tuple[bool, bool, Optional[str]]:
        if self.is_logged_in is False:
            account_has_been_logged_in = False
            new_auth_token_value = None
            fields_to_get = ["accountId", "username", "encryptedPassword"]

            account_data = self.engine_resources.accounts_data_dynamodb_client.get_account_by_email(
                email=username_or_email, fields_to_get=fields_to_get
            )
            if account_data is None:
                account_data = self.engine_resources.accounts_data_dynamodb_client.get_account_by_username(
                    username=username_or_email, fields_to_get=fields_to_get
                )

            if account_data is not None:
                print(account_data)
                account_data = AccountData(**account_data)

                if account_data.encryptedPassword is not None:
                    print(f"encrypted_password from the user : {encrypted_password}\n"
                          f"encrypted_password of the account : {account_data.encryptedPassword}")

                    if encrypted_password.lower() == account_data.encryptedPassword.lower():
                        # We lower the cases of both the passwords, to avoid issues of un-important conversion of the data
                        print("Password matched")
                        self.engine_resources.accounts_data_dynamodb_client.remove_old_auth_tokens(
                            account_id=account_data.accountId, fields_to_get=[]
                        )
                        new_auth_token_value = self.engine_resources.accounts_data_dynamodb_client.add_auth_token(account_id=account_data.accountId)
                        account_has_been_logged_in = True

                        self.is_logged_in = True
                        self.account_id = account_data.accountId
                        self.account_username = account_data.username
                    else:
                        print("Password did not match")
                else:
                    print(f"WARNING ! No password field has been found for user {username_or_email} with user_data : {account_data}")

                return True, account_has_been_logged_in, new_auth_token_value
            else:
                return False, account_has_been_logged_in, new_auth_token_value

    def login_with_cookies(self, cookies: Any) -> bool:
        from werkzeug.datastructures import ImmutableMultiDict
        if isinstance(cookies, (ImmutableMultiDict, dict)):
            account_id = cookies.get("lastLoggedWithAccountId")
            auth_token = cookies.get("authToken")

            if account_id is not None and isinstance(account_id, str) and auth_token is not None and isinstance(auth_token, str):
                return self._is_valid_auth_token_and_remove_old_tokens(account_id=account_id, auth_token=auth_token)
            else:
                return False
        else:
            raise Exception(f"Cookies must be of instance {ImmutableMultiDict} or {dict}")

    def check_for_permissions(self, project_owner_account_username: str, permissions_expressions: List[str]) -> Tuple[Optional[str], bool]:
        if self.is_logged_in is True and project_owner_account_username == self.account_username:
            print(f"Account being checked for permissions on a project that he owns. "
                  f"Permissions check not executed, and permissions approved."
                  f"\n  --project_owner_account_username:{project_owner_account_username}"
                  f"\n  --permissions_expressions(permissions_to_check):{permissions_expressions}")
            return self.account_id, True
        else:
            response = self.engine_resources.accounts_data_dynamodb_client.check_permissions_on_account_project(
                project_owner_account_username=project_owner_account_username,
                requester_account_id=self.account_id,
                permissions_to_check=permissions_expressions,
                fields_to_get=["accountId"]
            )
            if len(response.items) > 0:
                project_owner_account_data = AccountData(**response.items[0])
                print(f"Permissions approved for requester account for a project of another account."
                      f"\n  --project_owner_account_username:{project_owner_account_username}"
                      f"\n  --account_id(requester_account):{self.account_id}"
                      f"\n  --permissions_expressions(permissions_to_check):{permissions_expressions}"
                      f"\n  --project_owner_account_data(validated response data):{project_owner_account_data}")
                return project_owner_account_data.accountId, True
            else:
                print(f"Permissions not approved for requester account for a project of another account."
                      f"\n  --project_owner_account_username:{project_owner_account_username}"
                      f"\n  --account_id(requester_account):{self.account_id}"
                      f"\n  --permissions_expressions(permissions_to_check):{permissions_expressions}")
                return None, False
