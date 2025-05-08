# import logging
# from database.Database import DataBase

# class ColoredFormatter(logging.Formatter):
#     reset = "\033[0m"
#     black = "\033[0;30m"
#     red = "\033[0;31m"
#     green = "\033[0;32m"
#     yellow = "\033[0;33m"
#     blue = "\033[0;34m"
#     magenta = "\033[0;35m"
#     cyan = "\033[0;36m"
#     white = "\033[0;37m"

#     formats = {
#         logging.DEBUG: green + "%(asctime)s - %(name)s - DEBUG - %(message)s" + reset,
#         logging.INFO: white + "%(asctime)s - %(name)s - INFO - %(message)s" + reset,
#         logging.WARNING: yellow + "%(asctime)s - %(name)s - WARNING - %(message)s" + reset,
#         logging.ERROR: red + "%(asctime)s - %(name)s - ERROR - %(message)s" + reset,
#         logging.CRITICAL: magenta + "%(asctime)s - %(name)s - CRITICAL - %(message)s" + reset,
#     }

#     def format(self, record):
#         log_fmt = self.formats.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)

# class Logger:
#     def __init__(self, name_doc):
#         self.name_doc = name_doc
#         self.logger = logging.getLogger(name_doc)
        
#         # Убедитесь, что базовая конфигурация установлена только один раз
#         if not self.logger.hasHandlers():
#             logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#             handler = logging.StreamHandler()
#             handler.setFormatter(ColoredFormatter())
#             self.logger.addHandler(handler)

#     async def info(self, text: str):
#         db = DataBase()
#         await db.log_to_db("INFO", text, self.name_doc)
#         self.logger.info(text)

#     async def error(self, text: str):
#         db = DataBase()
#         await db.log_to_db("ERROR", text, self.name_doc)
#         self.logger.error(text)

#     async def warning(self, text: str):
#         db = DataBase()
#         await db.log_to_db("WARNING", text, self.name_doc)
#         self.logger.warning(text)


from database.Database import DataBase
import logging
# from datetime import datetime

class Logger:
    def __init__(self, name_doc):
        self.name_doc = name_doc
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(name_doc)

    async def info(self, text: str):
        db = DataBase()
        await db.log_to_db("INFO", text, self.name_doc)
        self.logger.info(text)

    async def error(self, text: str):
        db = DataBase()
        await db.log_to_db("ERROR", text, self.name_doc)
        self.logger.error(text)

    async def warning(self, text: str):
        db = DataBase()
        await db.log_to_db("WARNING", text, self.name_doc)
        self.logger.warning(text)
