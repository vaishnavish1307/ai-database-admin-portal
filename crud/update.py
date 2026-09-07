from sqlalchemy import (
    select,
    update
)

from sqlalchemy.orm import Session

from database.reflection import (
    get_table_object,
    get_primary_key
)

from services.audit_service import (
    log_action
)


def get_record_by_id(
    table_name,
    record_id,
    engine
):

    table = get_table_object(
        table_name
    )

    if table is None:
        return None

    if engine is None:
        return None

    pk = get_primary_key(
        table_name
    )

    if pk is None:
        return None

    try:

        with Session(engine) as session:

            stmt = (
                select(table)
                .where(
                    table.c[pk] == record_id
                )
            )

            result = session.execute(
                stmt
            ).first()

            if result:

                return dict(
                    result._mapping
                )

            return None

    except Exception as e:

        print(
            f"Error loading record: {e}"
        )

        return None


def update_record(
    table_name,
    record_id,
    data,
    engine
):

    table = get_table_object(
        table_name
    )

    if table is None:

        return (
            False,
            "Table not found"
        )

    if engine is None:

        return (
            False,
            "No active database connection"
        )

    pk = get_primary_key(
        table_name
    )

    if pk is None:

        return (
            False,
            "Primary key not found"
        )

    try:

        with Session(engine) as session:

            stmt = (
                update(table)
                .where(
                    table.c[pk] == record_id
                )
                .values(**data)
            )

            result = session.execute(
                stmt
            )

            session.commit()

            if result.rowcount == 0:

                return (
                    False,
                    "Record not found"
                )

        log_action(
            "SYSTEM",
            "UPDATE",
            table_name
        )

        return (
            True,
            "Record updated successfully"
        )

    except Exception as e:

        log_action(
            "SYSTEM",
            "UPDATE",
            table_name,
            "FAILED",
            str(e)
        )

        return (
            False,
            str(e)
        )