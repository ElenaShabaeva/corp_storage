from enum import Enum


class InviteStatus(str, Enum):
    SENT = "Отправлено"
    ACCEPTED = "Принято"
    DECLINED = "Отклонено"
