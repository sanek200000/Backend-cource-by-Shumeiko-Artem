from utils.db_manager import DBManager


class BaseServise:
    db: DBManager | None

    def __init__(self, db: DBManager | None = None):
        self.db = db
