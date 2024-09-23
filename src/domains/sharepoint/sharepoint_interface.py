import abc

from fastapi import Request

from src.models.requests.sharepoint_action_1_request import Action1Request, DownloadRequest
from src.models.responses.basic_response import BasicResponse

class ISharepointUseCase(abc.ABC):
    @abc.abstractmethod
    def action_1(self, request: Request) -> str:
        pass

    @abc.abstractmethod
    def action_2(self, request: Request, action_1_request: Action1Request) -> str:
        pass

    @abc.abstractmethod
    def download_files(self) -> str:
        pass

class ISharepointRepository(abc.ABC):
    @abc.abstractmethod
    def get_dealer_name(self, link_1: str) -> str:
        pass

    @abc.abstractmethod
    def read_forecast_columns(self, link_1: str) -> BasicResponse:
        pass

    @abc.abstractmethod
    def copy_forecast(self, sheet_name: str, forecast_data: dict, link_2: str) -> str:
        pass

    @abc.abstractmethod
    def get_dealer_name_two(self, link: str):
        pass

    @abc.abstractmethod
    def read_allocation_columns(self, link: str, sheet_name: str) -> BasicResponse:
        pass

    @abc.abstractmethod
    def copy_allocation(self, sheet_name: str, allocation_data: dict, link_2: str):
        pass

    @abc.abstractmethod
    def download_dealer_data(self, folder_name):
        pass

    @abc.abstractmethod
    def upload_excel(self, storage_dir, folder_name):
        pass

    @abc.abstractmethod
    def copy_forecast_from_folder(self, link: str, link_2: str):
        pass

    @abc.abstractmethod
    def copy_allocations_for_dealers(self):
        pass