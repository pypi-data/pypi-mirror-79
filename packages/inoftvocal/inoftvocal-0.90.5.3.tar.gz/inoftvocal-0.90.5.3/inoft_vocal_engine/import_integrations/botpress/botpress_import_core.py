import os
from pathlib import Path
from typing import Optional, List, Dict
from uuid import uuid4
from zipfile import ZipFile

from pydantic.dataclasses import dataclass

from inoft_vocal_engine.cloud_ressources.engine_resources import EngineResources
from inoft_vocal_engine.cloud_ressources.project_resources import ProjectResources
from inoft_vocal_engine.import_integrations.botpress.botpress_converter import BotpressConverter
from inoft_vocal_engine.utils.general import load_json
from inoft_vocal_engine.utils.paths import get_inoft_vocal_engine_root_path, get_engine_temp_path


@dataclass
class DiagramData:
    flow_data_dict: dict
    ui_data_dict: dict


class BotpressImportCore(BotpressConverter):
    def __init__(self, existing_extracted_archive_dirpath: Optional[str] = None,
                 source_zip_filepath: Optional[str] = None, source_zip_file_bytes: Optional[bytes] = None):
        self._existing_extracted_archive_dirpath = existing_extracted_archive_dirpath
        self._source_zip_filepath = source_zip_filepath
        self._source_zip_file_bytes = source_zip_file_bytes
        self._source_zip_filename = Path(self._source_zip_filepath).stem

        if self._existing_extracted_archive_dirpath is not None:
            self.extracted_archive_dirpath = self._existing_extracted_archive_dirpath
        else:
            self.extracted_archive_dirpath = os.path.join(get_engine_temp_path(), f"{self._source_zip_filename}_{uuid4()}")
            self._load_zip()
        self.extracted_archive_root_dirpath = os.path.join(self.extracted_archive_dirpath, self._source_zip_filename)

        self.flows_dirpath = os.path.join(self.extracted_archive_root_dirpath, "flows")

    def _load_zip(self):
        if self._source_zip_filepath is not None:
            bot_root_archive = ZipFile(self._source_zip_filepath)
            bot_root_archive.extractall(path=self.extracted_archive_dirpath)
        elif self._source_zip_file_bytes is not None:
            pass
        else:
            raise Exception(f"source_zip_filepath and source_zip_file_bytes cannot be both to None."
                            f"  --source_zip_filepath:{self._source_zip_filepath}"
                            f"  --source_zip_file_bytes:{self._source_zip_file_bytes}")

    def get_all_diagrams_data_from_zip(self) -> List[DiagramData]:
        diagrams_list: List[DiagramData] = list()

        if os.path.exists(self.flows_dirpath):
            for root, dirs, files in os.walk(self.flows_dirpath):
                for name in files:
                    current_filepath = os.path.join(root, name)
                    current_filepath_and_its_suffixes = current_filepath.split(".")
                    current_filepath_without_suffixes = current_filepath_and_its_suffixes[0]
                    current_filepath_suffixes = current_filepath_and_its_suffixes[1:]

                    if "json" in current_filepath_suffixes:
                        expected_flow_filepath = None
                        expected_ui_filepath = None

                        if "flow" in current_filepath_suffixes:
                            expected_flow_filepath = current_filepath
                            expected_ui_filepath = f"{current_filepath_without_suffixes}.ui.json"
                        elif "ui" in current_filepath_suffixes:
                            expected_ui_filepath = current_filepath
                            expected_flow_filepath = f"{current_filepath_without_suffixes}.flow.json"

                        if os.path.isfile(expected_flow_filepath) and os.path.isfile(expected_ui_filepath):
                            flow_data_dict = load_json(filepath=expected_flow_filepath)
                            ui_data_dict = load_json(filepath=expected_ui_filepath)
                            try:
                                diagrams_list.append(DiagramData(flow_data_dict=flow_data_dict, ui_data_dict=ui_data_dict))
                            except Exception as e:
                                print(f"{e} -- Error while trying to add new diagram with"
                                      f"  --flow_data_dict:{flow_data_dict}"
                                      f"  --ui_data_dict:{ui_data_dict}")

        return diagrams_list


if __name__ == "__main__":
    core = BotpressImportCore(
        existing_extracted_archive_dirpath="F:/Inoft/anvers_1944_project/inoft_vocal_engine/tmp/anvers_1944_787027a5-2aff-448c-979a-1cbfcffd9b3f",
        source_zip_filepath="C:/Users/LABOURDETTE/Documents/Software/BotPress/botpress-v12_8_1-win-x64/data/bots/anvers_1944.zip"
    )
    project_resources = ProjectResources(engine_resources=EngineResources(),
                                         account_username="robinsonlabourdette",
                                         project_url="anvers1944")

    diagrams_data = core.get_all_diagrams_data_from_zip()
    for diagram in diagrams_data:
        output = core.convert_diagram_files(project_resources=project_resources,
                                            diagram_flow_data_dict=diagram.flow_data_dict,
                                            diagram_ui_data_dict=diagram.ui_data_dict)
        print(output)
        for node in output:
            project_resources.project_diagrams_data_dynamodb_client.put_new_node(node_item=node)


