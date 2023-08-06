from typing import Optional, List, Any

from boto3.dynamodb.conditions import Key
from boto3.exceptions import ResourceNotExistsError
from pydantic import BaseModel

from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter, GlobalSecondaryIndex, PrimaryIndex, \
    Response, DynamoDBMapObjectSetter
from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils
from inoft_vocal_engine.import_integrations.botpress.engine_models import ProcessedNodeElement, NodeDatabaseItem, \
    NodeElementDataReceivedFromUser, DatabaseTransitionConditionItem
from inoft_vocal_engine.models.actions import BaseAction


class ProjectsDiagramsDataDynamoDbClient(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str):
        primary_index = PrimaryIndex(hash_key_name="nodeId", hash_key_variable_python_type=str)

        # todo: setup the global secondary indexes (they are currently a copy of the text contents database client)
        globals_secondary_indexes = [
            GlobalSecondaryIndex(hash_key_name="accountId", hash_key_variable_python_type=str, projection_type="ALL"),
            GlobalSecondaryIndex(hash_key_name="accountProjectId", hash_key_variable_python_type=str, projection_type="ALL"),
            GlobalSecondaryIndex(hash_key_name="accountProjectInstanceId", hash_key_variable_python_type=str, projection_type="ALL")
        ]
        super().__init__(table_name=table_name, region_name=region_name, primary_index=primary_index,
                         create_table=True, global_secondary_indexes=globals_secondary_indexes)

    def put_new_node(self, node_item: NodeDatabaseItem):
        self._put_item_dict(item_dict=node_item.dict())

    def _query_nodes_by_key(self, key_name: str, key_value: str) -> Response:
        return self._query_by_key(key_name=key_name, index_name=key_name, key_value=key_value)

    def query_nodes_by_instance_id(self, instance_id: str):
        response = self._query_nodes_by_key(key_name='accountProjectInstanceId', key_value=instance_id)
        return response

    def query_nodes_by_project_id(self, project_id: str) -> Response:
        response = self._query_nodes_by_key(key_name='accountProjectId', key_value=project_id)
        return response

    def _get_nodes_by_key(self, key_name: str, key_value: str) -> List[ProcessedNodeElement]:
        response = self._query_nodes_by_key(key_name=key_name, key_value=key_value)
        output_nodes: List[ProcessedNodeElement] = list()
        for item in response.items:
            if isinstance(item, dict):
                current_node_database_item = NodeDatabaseItem(**item)
                output_nodes.append(current_node_database_item.to_processed_node_element())
        return output_nodes

    def get_nodes_by_instance_id(self, instance_id: str) -> List[ProcessedNodeElement]:
        nodes = self._get_nodes_by_key(key_name='accountProjectInstanceId', key_value=instance_id)
        return nodes

    def get_nodes_by_project_id(self, project_id: str) -> List[ProcessedNodeElement]:
        nodes = self._get_nodes_by_key(key_name='accountProjectId', key_value=project_id)
        return nodes

    # todo: finish the client (update, get by latest, get by filter, and delete node)

    def update_node(self, node_element_data: NodeElementDataReceivedFromUser) -> Response:
        objects_setters: List[DynamoDBMapObjectSetter] = list()

        if node_element_data.nodeName is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="nodeName", value_to_set=node_element_data.nodeName))
        if node_element_data.nodeType is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="nodeType", value_to_set=node_element_data.nodeType))
        if node_element_data.actions is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="actions", value_to_set=node_element_data.actions))
        if node_element_data.transitions is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="transitions", value_to_set=node_element_data.transitions))
        if node_element_data.positionY is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="positionX", value_to_set=node_element_data.positionX))
        if node_element_data.positionY is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="positionY", value_to_set=node_element_data.positionY))
        if node_element_data.temp_on_receive is not None:
            objects_setters.append(DynamoDBMapObjectSetter(object_path="temp_on_receive", value_to_set=node_element_data.temp_on_receive))

        response = self._add_update_multiple_data_elements_to_map(
            key_name="nodeId", key_value=node_element_data.nodeId, objects_setters=objects_setters
        )
        return response

    def add_update_transition_to_node(self, transition_condition: DatabaseTransitionConditionItem) -> Response:
        response = self._add_update_data_element_to_map(
            key_name="nodeId", key_value=transition_condition.sourceNodeId,
            object_path_elements={"transitions": dict, transition_condition.transitionId: dict},
            element_values=transition_condition.to_database()
        )
        return response

    def add_update_action_to_node(self, action_instance: BaseAction) -> Response:
        # The real action_instance will not be of type BaseAction, but should always have BaseAction as of one of its parent.
        response = self._add_update_data_element_to_map(
            key_name="nodeId", key_value=action_instance.nodeId,
            object_path_elements={"actions": dict, action_instance.actionId: dict},
            element_values=action_instance.to_database()
        )
        return response


    """
    def get_latest_created(self, num_latest_items: int, exclusive_start_key: Optional[dict] = None) -> Response:
        return self._get_latest(index_name="stateId-creationTimestamp",
                                num_latest_items=num_latest_items, exclusive_start_key=exclusive_start_key)

    def get_latest_updated(self, num_latest_items: int, exclusive_start_key: Optional[dict] = None) -> Response:
        return self._get_latest(index_name="stateId-lastModificationTimestamp",
                                num_latest_items=num_latest_items, exclusive_start_key=exclusive_start_key)

    def get_by_id(self, account_project_id: str) -> (dict, bool):
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(TableName=self.table_name, Key={"elementId": account_project_id}, ConsistentRead=True)
            if "Item" in response:
                return Utils.dynamodb_to_python(dynamodb_object=response["Item"]), True
            else:
                return dict(), False
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process"
                            "of being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve attributes from DynamoDb table."
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")

    def get_by_character_name(self, character_name: str) -> Response:
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.scan(FilterExpression=Attr('characterNames').contains(character_name))
            if "Items" in response:
                return Response(Utils.dynamodb_to_python(dynamodb_object=response))
            else:
                return Response({})
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process"
                            "of being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve attributes from DynamoDb table."
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")

    def get_by_text_search(self, text_to_search: str) -> Response:
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.scan(FilterExpression=Attr('crudeText').contains(text_to_search))
            if "Items" in response:
                return Response(Utils.dynamodb_to_python(dynamodb_object=response))
            else:
                return Response({})
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process"
                            "of being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve attributes from DynamoDb table."
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")
    """

