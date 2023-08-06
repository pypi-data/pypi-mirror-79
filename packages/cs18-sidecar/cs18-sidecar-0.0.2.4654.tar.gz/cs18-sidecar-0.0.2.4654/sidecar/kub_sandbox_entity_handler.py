from abc import ABCMeta, abstractmethod
from typing import Dict


class IKubSandboxEntityHandler(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_entity_relative_path_under_namespace(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_annotations_from_entity_json(self, entity_json: dict) -> Dict[str, str]:
        raise NotImplementedError()

    @abstractmethod
    def get_entity_patch_json(self, annotations: Dict[str, str]) -> dict:
        raise NotImplementedError()


class ConfigMapSandboxEntityHandler(IKubSandboxEntityHandler):
    def __init__(self, sandbox_id: str) -> None:
        super().__init__()
        self._sandbox_id = sandbox_id

    def get_entity_relative_path_under_namespace(self) -> str:
        return f'/configmaps/{self._sandbox_id}'

    def get_annotations_from_entity_json(self, entity_json: dict) -> Dict[str, str]:
        return entity_json["data"]

    def get_entity_patch_json(self, annotations: Dict[str, str]) -> dict:
        data_json = {
            'data': annotations
        }
        return data_json


# class NamespaceSandboxEntityHandler(IKubSandboxEntityHandler):
#     def get_entity_relative_path_under_namespace(self) -> str:
#         return ''
#
#     def get_annotations_from_entity_json(self, entity_json: dict) -> Dict[str, str]:
#         return entity_json["metadata"]["annotations"]
#
#     def get_entity_patch_json(self, annotations: Dict[str, str]) -> dict:
#         data_json = {
#             'metadata': {
#                 'annotations': annotations
#             }
#         }
#         return data_json
