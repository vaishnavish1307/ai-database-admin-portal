from sqlalchemy import insert
from sqlalchemy.orm import Session

from database.reflection import (
    get_table_object
)

from services.audit_service import (
    log_action
)


def insert_record(
    table_name,
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

    try:

        # Convert boolean values for MySQL
        for key, value in data.items():

            if isinstance(value, bool):

                data[key] = (
                    1 if value else 0
                )

        with Session(engine) as session:

            stmt = (
                insert(table)
                .values(**data)
            )

            session.execute(stmt)

            session.commit()

        log_action(
            "SYSTEM",
            "INSERT",
            table_name
        )

        return (
            True,
            "Record inserted successfully"
        )

    except Exception as e:

        log_action(
            "SYSTEM",
            "INSERT",
            table_name,
            "FAILED",
            str(e)
        )

        return (
            False,
            str(e)
        )