from typing import Optional

from ipapp.config import BaseConfig
from ipapp.logger.adapters.requests import RequestsConfig
from ipapp.logger.adapters.zipkin import ZipkinConfig
from pydantic import Field


class MaskZipkinConfig(ZipkinConfig):
    masking_sensitive_data: bool = Field(
        True, description="Флаг маскирования чувствительных данных",
    )


class MaskRequestsConfig(RequestsConfig):
    masking_sensitive_data: bool = Field(
        True, description="Флаг маскирования чувствительных данных",
    )


class MaskConfig(BaseConfig):
    rule: Optional[str] = Field(None, description="Правила маскирования данных")
