from typing import Annotated
from auth.auth import auth_backend
from fastapi import APIRouter, Body, Depends
from fastapi import APIRouter, status
from fastapi_users import FastAPIUsers
from sqlalchemy import select, insert, delete, update
from auth.manager import get_user_manager
from auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from operation.models import operation
from fastapi import HTTPException
from operation.schemas import RequestOperation, ResponseOperation, RequestOperationSuper

from database import get_async_session


route = APIRouter(prefix="/operation", tags=["operation"])

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

c_user = fastapi_users.current_user()  # c_user = current_user


@route.post("/post", status_code=status.HTTP_201_CREATED)
async def set_operations(
    new_operation: RequestOperation,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(c_user),
):
    stmt = (
        insert(operation)
        .values(
            user_id=user.id,
            buy=new_operation.buy,
            figi=new_operation.figi,
            price=new_operation.price,
            count=new_operation.count,
            date=new_operation.date.replace(tzinfo=None),
        )
        .returning(operation.c.id)
    )
    result = await session.execute(stmt)
    await session.commit()
    record = result.first()
    id = record[0] if record else None
    return {
        "content": "the record was created successfully",
        "record ID": id,
    }


@route.get("/get")
async def get_operations(
    session: AsyncSession = Depends(get_async_session), user: User = Depends(c_user)
) -> list[ResponseOperation]:
    query = select(operation).where(operation.c.user_id == user.id)
    result = await session.execute(query)
    await session.commit()
    content = list()
    for i in result.all():
        content.append(i._asdict())
    return content


@route.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_operation(
    operation_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(c_user),
):
    stmt = (
        delete(operation)
        .where(operation.c.id == operation_id)
        .returning(operation.c.id)
    ).returning(operation.c.id)
    result = await session.execute(stmt)
    await session.commit()
    record = result.first()
    id = record[0] if record else None
    if record:
        return
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is no record with the specified number",
        )


@route.put("/put", status_code=status.HTTP_202_ACCEPTED)
async def change_operation(
    operation_id: Annotated[int, Body()],
    new_operation: RequestOperation,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(c_user),
):
    stmt = (
        update(operation)
        .where(operation.c.id == operation_id, operation.c.user_id == user.id)
        .values(
            user_id=user.id,
            buy=new_operation.buy,
            price=new_operation.price,
            count=new_operation.count,
            date=new_operation.date.replace(tzinfo=None),
        )
    ).returning(operation.c.id)
    result = await session.execute(stmt)
    await session.commit()
    record = result.first()
    id = record[0] if record else None
    if id:
        return {
            "content": "the record has been successfully changed",
            "record ID": id,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="there is no record with the specified number",
        )


@route.post("/post-super", status_code=status.HTTP_202_ACCEPTED)
async def set_operations(
    new_operation: RequestOperationSuper,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(c_user),
):
    if user.is_superuser:
        stmt = (
            insert(operation)
            .values(
                user_id=new_operation.user_id,
                buy=new_operation.buy,
                figi=new_operation.figi,
                price=new_operation.price,
                count=new_operation.count,
                date=new_operation.date.replace(tzinfo=None),
            )
            .returning(operation.c.id)
        )
        result = await session.execute(stmt)
        await session.commit()
        record = result.first()
        id = record[0] if record else None
        return {
            "content": "the record was created successfully",
            "record ID": id,
        }
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not a super user"
        )


@route.put("/put-super", status_code=status.HTTP_202_ACCEPTED)
async def change_operation(
    operation_id: int,
    new_operation: RequestOperationSuper,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(c_user),
):
    if user.is_superuser:
        stmt = (
            update(operation)
            .where(
                operation.c.id == operation_id,
                operation.c.user_id == new_operation.user_id,
            )
            .values(
                user_id=new_operation.user_id,
                buy=new_operation.buy,
                price=new_operation.price,
                count=new_operation.count,
                date=new_operation.date.replace(tzinfo=None),
            )
        ).returning(operation.c.id)
        result = await session.execute(stmt)
        await session.commit()
        record = result.first()
        id = record[0] if record else None
        if id:
            return {
                "content": "the record has been successfully changed",
                "record ID": id,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="there is no record with the specified number",
            )
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not a super user"
        )


@route.delete("/delete-super", status_code=status.HTTP_204_NO_CONTENT)
async def delete_operation(
    operation: int,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(c_user),
):
    if user.is_superuser:
        stmt = (
            delete(operation)
            .where(operation.c.id == operation.id, operation.c.user_id == user_id)
            .returning(operation.c.id)
        )
        result = await session.execute(stmt)
        await session.commit()
        if result.first():
            return
        else:
            raise HTTPException(
                status_code=404,
                detail="this user does not have an entry with this number",
            )
    else:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not a super user"
        )
