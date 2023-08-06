from typing import List

from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ProjectsTextContentsDynamoDbClient
from inoft_vocal_engine.import_integrations.botpress.botpress_converter import BotpressConverter


def put_new_botpress_contents_from_list(contents_list: list, project_resources: ProjectResources):
    from inoft_vocal_engine.import_integrations.botpress.utils import botpress_date_to_timestamp

    contents_list = BotpressConverter().botpress_contents_json_object_to_list_content_elements(list_all_text_elements=contents_list)
    for content in contents_list:
        from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ContentDatabaseItem
        db_item = ContentDatabaseItem(elementId=content.id, stateId=0,
                                      creationTimestamp=botpress_date_to_timestamp(content.created_on),
                                      lastModificationTimestamp=botpress_date_to_timestamp(content.modified_on),
                                      crudeText=content.crude_text, characterNames=content.character_names)
        project_resources.project_text_contents_dynamodb_client.put_new_content(db_item)

def put_new_botpress_contents_from_filepath(filepath: str, project_resources: ProjectResources):
    contents_list = BotpressConverter().botpress_json_file_to_list_content_elements(filepath=filepath)
    put_new_botpress_contents_from_list(contents_list=contents_list, project_resources=project_resources)
