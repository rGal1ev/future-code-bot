MODULES_TABLE = """
    CREATE TABLE IF NOT EXISTS Modules (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        
        NUMBER INTEGER NOT NULL,
        TITLE TEXT NOT NULL
    );
"""

TASKS_TABLE = """
    CREATE TABLE IF NOT EXISTS Tasks (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        
        TITLE TEXT NOT NULL,
        NUMBER INTEGER NOT NULL,
        MIN_ANSWERS_COUNT INTEGER NOT NULL,
        MODULE_ID INTEGER REFERENCES Modules(ID)
    );
"""

TASK_ANSWERS_TABLE = """
    CREATE TABLE IF NOT EXISTS TaskAnswers (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        
        VALUE TEXT NOT NULL,
        NUMBER INTEGER NOT NULL,
        TASK_ID INTEGER REFERENCES Tasks(ID)
    );
"""

TEST_ANSWERS_TABLE = """
    CREATE TABLE IF NOT EXISTS TestAnswers (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        
        VALUE TEXT NOT NULL,
        NUMBER INTEGER NOT NULL,
        MODULE_ID INTEGER REFERENCES Modules(ID)
    );
"""

TABLES_INIT_LIST = [
    MODULES_TABLE,
    TASKS_TABLE,

    TASK_ANSWERS_TABLE,
    TEST_ANSWERS_TABLE
]
