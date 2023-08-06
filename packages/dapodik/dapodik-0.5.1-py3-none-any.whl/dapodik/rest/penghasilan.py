from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik import DapodikObject
from dapodik.utils.decorator import set_meta


@set_meta('penghasilan_id')
@dataclass(eq=False, frozen=True)
class Penghasilan(DapodikObject):
    penghasilan_id: int
    nama: str
    batas_bawah: int
    batas_atas: int
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
