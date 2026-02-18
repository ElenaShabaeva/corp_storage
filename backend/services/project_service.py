from fastapi import HTTPException, status
from utils.jwt_utils import decode_jwt
from jwt import ExpiredSignatureError, DecodeError
from utils.uow import UnitOfWork
from uuid import UUID
from datetime import datetime
from services.notification_service import notification_service
from schemas.request.project_request import (
    ProjectCreateRequestSchema,
    InviteKickUserRequestSchema
)
from schemas.internal.user_schema import (
    UserShortInfoSchema
)
from schemas.internal.notification_schema import (
    InviteNotificationSchema,
    MessageNotificationSchema
)
from schemas.internal.invite_status_enum import InviteStatus
from schemas.response.project_response import (
    ProjectShortInfoResponseSchema,
    GetAllProjectsResponseSchema,
    ProjectMainPageInfoResponseSchema,
    ProjectMembersResponseSchema
)
from schemas.response.standart_message import MessageResponseSchema


class ProjectService:
    def __init__(self):
        self.uow = UnitOfWork()

    async def get_all(self, access_token: str | None) -> GetAllProjectsResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                projects = await self.uow.projects.get_all(user_id=user_id)
            projects_response = [ProjectShortInfoResponseSchema(
                id=project.id,
                name=project.name,
                creator_login=project.creator.login,
                members_count=project.members_count
            ) for project in projects]
            return GetAllProjectsResponseSchema(
                count=len(projects_response),
                projects=projects_response
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def create(
            self,
            payload: ProjectCreateRequestSchema,
            access_token: str | None
    ) -> ProjectShortInfoResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                new_project = await self.uow.projects.post(
                    name=payload.name,
                    description=payload.description,
                    creator_id=user_id
                )
                await self.uow.user_project_association.add_member(
                    user_id=user_id,
                    project_id=new_project.id
                )
                new_project.members_count += 1
                user = await self.uow.users.get_by_id(user_id=user_id)
            return ProjectShortInfoResponseSchema(
                id=new_project.id,
                name=new_project.name,
                creator_login=user.login,
                members_count=new_project.members_count
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def get_by_id(self, project_id: UUID, access_token: str | None) -> ProjectMainPageInfoResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=project_id)
                if not project:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Проект не найден"
                    )
                members = await self.uow.projects.get_members(project_id=project_id)
                if user_id not in [user.id for user in members]:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Нет прав"
                    )

            return ProjectMainPageInfoResponseSchema(
                id=project.id,
                name=project.name,
                description=project.description,
                isOwner=True if project.creator_id == user_id else False
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def get_members(self, project_id: UUID, access_token: str | None) -> ProjectMembersResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=project_id)
                members = await self.uow.projects.get_members(project_id=project_id)
                if user_id not in [user.id for user in members]:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Нет прав"
                    )

            return ProjectMembersResponseSchema(
                members_count=project.members_count,
                members=[UserShortInfoSchema(
                    id=member.id,
                    login=member.login
                ) for member in members]
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def invite_user(self, payload: InviteKickUserRequestSchema, access_token: str | None) -> MessageResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=payload.project_id)
                if project.creator_id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Добавлять нового участника может только создатель проекта"
                    )

                members = await self.uow.projects.get_members(project_id=payload.project_id)
                new_user_in_project = await self.uow.users.get_by_login(login=payload.login)
                if new_user_in_project.id in [member.id for member in members]:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Пользователь уже состоит в данном проекте"
                    )

                invite_notification = await self.uow.invite_notifications.get_sent_by_user_and_project_ids(
                    to_user_id=new_user_in_project.id,
                    project_id=project.id
                )
                if invite_notification:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Пользователь уже приглашен"
                    )

                creator = await self.uow.users.get_by_id(user_id=project.creator_id)
                date_time = datetime.now()
                invite_db = await self.uow.invite_notifications.post(
                    project_id=project.id,
                    invite_datetime=date_time,
                    from_user_id=user_id,
                    to_user_id=new_user_in_project.id
                )
                await notification_service.send_notification(
                    user_id=new_user_in_project.id,
                    notification=InviteNotificationSchema(
                        id=invite_db.id,
                        project_name=project.name,
                        project_creator=creator.login,
                        date_time=date_time.strftime("%d.%m.%Y / %H:%M"),
                        state=invite_db.state
                    )
                )
            return MessageResponseSchema(
                status="success",
                message="Приглашение в проект успешно отправлено"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def accept_invite(self, invite_id: UUID, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                invite = await self.uow.invite_notifications.get_by_id(invite_id=invite_id)
                if not invite:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Приглашение не найдено"
                    )
                if invite.state == InviteStatus.ACCEPTED or invite.state == InviteStatus.DECLINED:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Приглашение уже принято или отклонено"
                    )
                await self.uow.user_project_association.add_member(
                    user_id=invite.to_user_id,
                    project_id=invite.project_id
                )
                invite.project.members_count += 1
                invite.state = InviteStatus.ACCEPTED
                invited_user = await self.uow.users.get_by_id(user_id=invite.to_user_id)

                date_time = datetime.now()
                message = f"{invited_user.login} принял приглашение в {invite.project.name}"
                message_db = await self.uow.message_notifications.post(
                    message=message,
                    message_datetime=date_time,
                    from_user_id=invite.to_user_id,
                    to_user_id=invite.from_user_id
                )

                await notification_service.send_notification(
                    user_id=invite.from_user_id,
                    notification=MessageNotificationSchema(
                        id=message_db.id,
                        message=message,
                        date_time=date_time.strftime("%d.%m.%Y / %H:%M")
                    )
                )

            return MessageResponseSchema(
                status="success",
                message="Приглашение принято"
            )

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def decline_invite(self, invite_id: UUID, access_token: str | None):
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)

            async with self.uow.start():
                invite = await self.uow.invite_notifications.get_by_id(invite_id=invite_id)
                if not invite:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Приглашение не найдено"
                    )
                if invite.state == InviteStatus.ACCEPTED or invite.state == InviteStatus.DECLINED:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Приглашение уже принято или отклонено"
                    )
                invite.state = InviteStatus.DECLINED
                invited_user = await self.uow.users.get_by_id(user_id=invite.to_user_id)

                date_time = datetime.now()
                message = f"{invited_user.login} отклонил приглашение в {invite.project.name}"
                message_db = await self.uow.message_notifications.post(
                    message=message,
                    message_datetime=date_time,
                    from_user_id=invite.to_user_id,
                    to_user_id=invite.from_user_id
                )
                await notification_service.send_notification(
                    user_id=invite.from_user_id,
                    notification=MessageNotificationSchema(
                        id=message_db.id,
                        message=message,
                        date_time=date_time.strftime("%d.%m.%Y / %H:%M")
                    )
                )
            return MessageResponseSchema(
                status="success",
                message="Приглашение отклонено"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def leave(self, project_id: UUID, access_token: str | None) -> MessageResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=project_id)
                if project.creator_id != user_id:
                    await self.uow.user_project_association.delete(user_id=user_id, project_id=project_id)
                    project.members_count -= 1
                else:
                    await self.uow.projects.delete(project_id=project_id)

            return MessageResponseSchema(
                status="success",
                message="Выход прошел успешно"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )

    async def kick_member(
            self,
            access_token: str | None,
            payload: InviteKickUserRequestSchema
    ) -> MessageResponseSchema:
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен не найден"
            )
        try:
            user_id, _ = decode_jwt(token=access_token)
            async with self.uow.start():
                project = await self.uow.projects.get_by_id(project_id=payload.project_id)
                if not project:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Проект не найден"
                    )
                if user_id != project.creator_id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Нет прав"
                    )
                user = await self.uow.users.get_by_login(login=payload.login)
                if user.id == user_id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Нельзя выгнать создателя"
                    )
                members = await self.uow.projects.get_members(project_id=project.id)
                if user not in members:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Пользователя уже нет в проекте"
                    )
                await self.uow.user_project_association.delete(user_id=user.id, project_id=project.id)
                project.members_count -= 1
            return MessageResponseSchema(
                status="success",
                message="Пользователь успешно выгнан из проекта"
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access токен истек"
            )
        except DecodeError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный формат токена"
            )
