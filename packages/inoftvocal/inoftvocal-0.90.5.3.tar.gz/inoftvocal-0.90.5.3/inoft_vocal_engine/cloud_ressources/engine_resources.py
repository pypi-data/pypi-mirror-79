from pydantic import validate_arguments
from inoft_vocal_engine.databases.dynamodb.accounts_data_dynamodb_client import UsersDynamoDBClient


# todo: make engine resources access static, instead of creating a new class on each lambda invocation ?
class EngineResources:
    _accounts_data_dynamodb_client = None
    _users_dynamodb_table_name = "inoft-vocal-engine_accounts-data"

    @validate_arguments
    def __init__(self):
        pass

    @property
    def accounts_data_dynamodb_client(self) -> UsersDynamoDBClient:
        if self._accounts_data_dynamodb_client is None:
            self._accounts_data_dynamodb_client = UsersDynamoDBClient(
                table_name=self._users_dynamodb_table_name, region_name="eu-west-2"
            )
        return self._accounts_data_dynamodb_client

