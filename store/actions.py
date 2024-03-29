import aiosqlite
from os import getenv

SQLITE_PATH = getenv("SQLITE_PATH")


async def get_modules() -> list[dict]:
    modules = []

    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        async with connection.execute("SELECT * FROM Modules ORDER BY NUMBER") as cursor:
            async for row in cursor:
                modules.append({
                    "id": row["ID"],
                    "title": row["TITLE"],
                    "number": row["NUMBER"]
                })

            return modules


async def get_module_by_id(module_id: int) -> dict:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        async with connection.execute(f"SELECT * FROM Modules WHERE ID = {module_id}") as cursor:
            async for row in cursor:
                return {
                    "id": row["ID"],
                    "title": row["TITLE"],
                    "number": row["NUMBER"]
                }


async def add_module(number: int, title: str):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        cursor = await connection.cursor()

        await cursor.execute("INSERT INTO Modules(NUMBER, TITLE) VALUES (?, ?);", [number, title])
        module_id = cursor.lastrowid

        await connection.commit()
        return module_id


async def delete_module(module_id: int):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        await connection.execute(f"DELETE FROM Modules WHERE ID = {module_id}")
        await connection.commit()


async def update_module(module_id: int, title: str, number: int):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        await connection.execute("""
            UPDATE Modules
            SET NUMBER = ?,
                TITLE = ?

            WHERE
                ID = ?
        """, [number, title, module_id])

        await connection.commit()


async def get_tasks(module_id: int) -> list[dict]:
    tasks = []
    sql = f"""
        SELECT * FROM Tasks
        WHERE MODULE_ID = {module_id}
        ORDER BY NUMBER
    """

    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        async with connection.execute(sql) as cursor:
            async for row in cursor:
                tasks.append({
                    "id": row["ID"],
                    "title": row["TITLE"],
                    "number": row["NUMBER"],
                    "min_answers_count": row["MIN_ANSWERS_COUNT"],
                    "module_id": row["MODULE_ID"]
                })

            return tasks


async def get_task_by_id(task_id: int) -> dict:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        async with connection.execute(f"SELECT * FROM Tasks WHERE ID = {task_id}") as cursor:
            async for row in cursor:
                return {
                    "id": row["ID"],
                    "title": row["TITLE"],
                    "number": row["NUMBER"],
                    "min_answers_count": row["MIN_ANSWERS_COUNT"],
                    "module_id": row["MODULE_ID"]
                }


async def add_task(title: str, number: int,
                   min_answers_count: int, module_id: int):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        cursor = await connection.cursor()

        await cursor.execute(
            "INSERT INTO Tasks(TITLE, NUMBER, MIN_ANSWERS_COUNT, MODULE_ID) VALUES (?, ?, ?, ?);",
            [title,
             number,
             min_answers_count,
             module_id])

        task_id = cursor.lastrowid

        await connection.commit()
        return task_id

# async def add_task(title: str, number: int,
#                    min_answers_count: int, module_id: int):
#     async with aiosqlite.connect(SQLITE_PATH) as connection:
#         await connection.execute(
#             "INSERT INTO Tasks(TITLE, NUMBER, MIN_ANSWERS_COUNT, MODULE_ID) VALUES (?, ?, ?, ?);",
#             [title,
#              number,
#              min_answers_count,
#              module_id])
#
#         await connection.commit()
#
#         task_id = connection.
#         return task_id


async def delete_task(task_id: int) -> bool:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        await connection.execute(f"DELETE FROM Tasks WHERE ID = {task_id}")
        await connection.commit()

        return connection.total_changes > 0


async def update_task(task_id: int, title: str, number: int,
                      min_answers_count: int, module_id: int):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        await connection.execute("""
            UPDATE Tasks
            SET NUMBER = ?,
                TITLE = ?,
                MIN_ANSWERS_COUNT = ?,
                MODULE_ID = ?

            WHERE
                ID = ?
        """, [number, title, min_answers_count, module_id, task_id])

        await connection.commit()


async def get_task_answers(task_id: int) -> list[dict]:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        task_answers = []
        connection.row_factory = aiosqlite.Row

        async with connection.execute(f"SELECT * FROM TaskAnswers WHERE TASK_ID = {task_id} ORDER BY NUMBER") as cursor:
            async for row in cursor:
                task_answers.append({
                    "id": row["ID"],
                    "value": row["VALUE"],
                    "number": row["NUMBER"]
                })
            return task_answers


async def get_task_answer_by_id(task_answer_id: int) -> dict:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        async with connection.execute(f"SELECT * FROM TaskAnswers WHERE ID = {task_answer_id}") as cursor:
            async for row in cursor:
                return {
                    "id": row["ID"],
                    "value": row["VALUE"],
                    "number": row["NUMBER"]
                }


async def add_task_answer(task_id: int, number: int, value: str) -> None:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        await connection.execute("""
            INSERT INTO TaskAnswers(VALUE, NUMBER, TASK_ID) VALUES (?, ?, ?)
        """, [value, number, task_id])

        await connection.commit()


async def update_task_answer_by_id(task_answer_id: int, number: int, value: str) -> None:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        await connection.execute("""
            UPDATE TaskAnswers
            SET NUMBER = ?,
                VALUE = ?
            
            WHERE
                ID = ?
        """, [number, value, task_answer_id])

        await connection.commit()


async def delete_task_answer_by_id(task_answer: int):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        await connection.execute(f"DELETE FROM TaskAnswers WHERE ID = {task_answer}")
        await connection.commit()


async def get_test_answers(module_id: int) -> list[dict]:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        test_answers = []
        connection.row_factory = aiosqlite.Row

        async with connection.execute(
                f"SELECT * FROM TestAnswers WHERE MODULE_ID = {module_id} ORDER BY NUMBER") as cursor:
            async for row in cursor:
                test_answers.append({
                    "id": row["ID"],
                    "number": row["NUMBER"],
                    "value": row["VALUE"]
                })

            return test_answers


async def update_test_answer(test_answer_id: int, number: int, value: str):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        await connection.execute("""
            UPDATE TestAnswers
            SET NUMBER = ?,
                VALUE = ?

            WHERE
                ID = ?
        """, [number, value, test_answer_id])

        await connection.commit()


async def add_test_answer(module_id: int, number: int, value: str) -> None:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        await connection.execute("""
            INSERT INTO TestAnswers(VALUE, NUMBER, MODULE_ID) VALUES (?, ?, ?)
        """, [value, number, module_id])

        await connection.commit()


async def get_test_answer_by_id(test_answer_id: int) -> dict:
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        connection.row_factory = aiosqlite.Row

        async with connection.execute(f"SELECT * FROM TestAnswers WHERE ID = {test_answer_id}") as cursor:
            async for row in cursor:
                return {
                    "id": row["ID"],
                    "number": row["NUMBER"],
                    "value": row["VALUE"]
                }


async def delete_test_answer_by_id(test_answer: int):
    async with aiosqlite.connect(SQLITE_PATH) as connection:
        await connection.execute(f"DELETE FROM TestAnswers WHERE ID = {test_answer}")
        await connection.commit()
