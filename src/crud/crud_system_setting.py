from src.db.models.system_setting import SystemSetting
from src.schemas.system_setting import (
    SystemSettingsCreate,
    SystemSettingsUpdate,
)

from .base import CRUDBase


class CRUDSystemSetting(CRUDBase[SystemSetting, SystemSettingsCreate, SystemSettingsUpdate]):
    pass


system_setting = CRUDSystemSetting(SystemSetting)
