from typing import Any, Coroutine
from fastapi import HTTPException, Depends
from starlette.requests import Request
from passlib.context import CryptContext
import datetime
import environ
import os
from src.domains.sharepoint.sharepoint_repository import SharepointRepository
from src.models.requests.sharepoint_action_1_request import Action1Request, DownloadRequest
from src.config.config import get_config
from src.domains.sharepoint.sharepoint_interface import ISharepointRepository, ISharepointUseCase


class SharepointUseCase(ISharepointUseCase):
    def __init__(self, sharepoint_repository: ISharepointRepository = Depends(SharepointRepository)):
        self.sharepoint_repository = sharepoint_repository

    def download_files(self, request: Request) -> str:
        env = environ.Env()
        environ.Env.read_env()
        SHAREPOINT_DEALER_DATA = env('SHAREPOINT_DEALER_DATA')
        SHAREPOINT_TO_BE_MACROED = env('SHAREPOINT_TO_BE_MACROED')
        dealer_data = self.sharepoint_repository.download_dealer_data(SHAREPOINT_DEALER_DATA)
        download_macro_excel = self.sharepoint_repository.download_dealer_data(SHAREPOINT_TO_BE_MACROED)
        print(dealer_data)
        print(download_macro_excel)
        return dealer_data
        
    def action_1(self, request: Request) -> str:
        # dealer_name = self.sharepoint_repository.get_dealer_name(action_1_request.link_1)
        # forecast_data = self.sharepoint_repository.read_forecast_columns(action_1_request.link_1)
        # data = self.sharepoint_repository.copy_forecast(dealer_name, forecast_data, action_1_request.link_2)
        env = environ.Env()
        environ.Env.read_env()
        SHAREPOINT_DEALER_DATA = env('SHAREPOINT_DEALER_DATA')
        SHAREPOINT_TO_BE_MACROED = env('SHAREPOINT_TO_BE_MACROED')
        dealer_data = self.sharepoint_repository.download_dealer_data(SHAREPOINT_DEALER_DATA)
        macro_excel = self.sharepoint_repository.download_dealer_data(SHAREPOINT_TO_BE_MACROED)

        data = self.sharepoint_repository.copy_forecast_from_folder(dealer_data, macro_excel)
        return data
    
    def action_2(self, request: Request) -> str:
        # dealer_name = self.sharepoint_repository.get_dealer_name_two(action_1_request.link_2)
        # allocation_data = self.sharepoint_repository.read_allocation_columns(action_1_request.link_1, dealer_name)
        # data = self.sharepoint_repository.copy_allocation(dealer_name, allocation_data, action_1_request.link_2)
        env = environ.Env()
        environ.Env.read_env()
        SHAREPOINT_TO_BE_MACROED = env('SHAREPOINT_TO_BE_MACROED')
        SHAREPOINT_DEALER_FINAL_ALLOCATION = env('SHAREPOINT_DEALER_FINAL_ALLOCATION')
        macro_excel = self.sharepoint_repository.download_dealer_data(SHAREPOINT_TO_BE_MACROED)
        dealer_final = self.sharepoint_repository.download_dealer_data(SHAREPOINT_DEALER_FINAL_ALLOCATION)
        data = self.sharepoint_repository.copy_allocations_for_dealers(macro_excel, dealer_final)
        return data