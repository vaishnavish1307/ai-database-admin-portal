import pandas as pd

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.reflection import get_table_object


def get_table_data(
    table_name,
    engine
):
    """
    Fetch all records from the selected table
    using the currently active database engine.
    """

    table = get_table_object(
        table_name
    )

    if table is None:
        return pd.DataFrame()

    if engine is None:
        return pd.DataFrame()

    try:

        with Session(engine) as session:

            stmt = select(table)

            result = session.execute(
                stmt
            )

            rows = result.fetchall()

            if not rows:
                return pd.DataFrame()

            return pd.DataFrame(
                rows,
                columns=result.keys()
            )

    except Exception as e:

        print(
            f"Error reading table {table_name}: {e}"
        )

        return pd.DataFrame()