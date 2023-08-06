from boto3.dynamodb.conditions import Attr
from boto3.exceptions import ResourceNotExistsError
from typing import List, Dict, Optional

from pydantic import ValidationError

from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter, PrimaryIndex, Response
from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils
from inoft_vocal_engine.vocal_apps_model_schemas.models import InoftVocalEngineModelSchema


class VocalAppsModelSchemasDynamoDBClient(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str):
        primary_index = PrimaryIndex(hash_key_name="accountProjectId", hash_key_variable_python_type=str)
        super().__init__(table_name=table_name, region_name=region_name, primary_index=primary_index, create_table=True)

    def set_update_one_intent(self, accountProjectId: str, intent_model: InoftVocalEngineModelSchema.IntentModel) -> Response:
        response = self._add_update_data_element_to_map(
            key_name="accountProjectId", key_value=accountProjectId,
            object_path_elements={"intents": dict, intent_model.intentId: dict},
            element_values=intent_model.dict()
        )
        return response

    def put_model_schema(self, account_project_id: str, model_schema: InoftVocalEngineModelSchema) -> Response:
        from inoft_vocal_engine.vocal_apps_model_schemas.models import InoftVocalEngineModelSchemaDatabaseComplete
        model_schema = InoftVocalEngineModelSchemaDatabaseComplete(
            accountProjectId=account_project_id, **model_schema.dict()
        )
        response = self._put_item_dict(model_schema.dict())
        return response

    def query_all_intents_by_account_project_id(self, account_project_id: str) -> dict:
        response = self._query_by_key(key_name="accountProjectId", key_value=account_project_id,
                                      fields_to_get=["intents"], query_limit=1)
        if response.count == 1:
            if "intents" in response.items[0]:
                return response.items[0]["intents"]
            else:
                return dict()
        elif response.count > 1:
            print(f"WARNING ! When calling the function {self.query_all_intents_by_account_project_id}, "
                  f"more than one items has been returned with the same accountProjectId."
                  f"  --accountProjectId:{account_project_id}"
                  f"  --response.items:{response.items}"
                  f"  --response.count:{response.count}")
        return dict()

    def get_all_intents_instances_by_account_project_id(self, account_project_id: str) -> List[InoftVocalEngineModelSchema.IntentModel]:
        output_intents_list: List[InoftVocalEngineModelSchema.IntentModel] = list()

        response_intents_dict = self.query_all_intents_by_account_project_id(account_project_id=account_project_id)
        for intent_values in response_intents_dict.values():
            try:
                output_intents_list.append(InoftVocalEngineModelSchema.IntentModel(**intent_values))
            except ValidationError as e:
                print(f"Validation Error while validating an IntentModel from the database : {e}")

        return output_intents_list

    def get_all_intents_dicts_by_account_project_id(self, account_project_id: str) -> List[dict]:
        output_intents_list: List[dict] = list()

        response_intents_dict = self.query_all_intents_by_account_project_id(account_project_id=account_project_id)
        for intent_values in response_intents_dict.values():
            try:
                output_intents_list.append(InoftVocalEngineModelSchema.IntentModel(**intent_values).dict())
            except ValidationError as e:
                print(f"Validation Error while validating an IntentModel from the database : {e}")

        return output_intents_list

    def update_value_with_path_target(self, account_project_id: str, object_path_elements: Dict[str, type], value: any):
        update_item_response = self._add_update_data_element_to_map(
            key_name="accountProjectId", key_value=account_project_id,
            object_path_elements=object_path_elements, element_values=value
        )
        return update_item_response

    def get_item_in_path_target(self, account_project_id: str, target_path_elements: Dict[str, type]) -> Optional[dict]:
        return self._get_item_in_path_target(
            key_name="accountProjectId", key_value=account_project_id,
            target_path_elements=target_path_elements
        )
