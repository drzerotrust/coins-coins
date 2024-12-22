import logging
from colorama import Fore, Style, init

init(autoreset=True)

class CustomFormatter(logging.Formatter):
    x_id = "[@drzerotrust]$ "
    
    def format(self, record):
        if record.levelno == logging.ERROR:
            level_color = Fore.RED
        elif record.levelno == logging.WARNING:
            level_color = Fore.YELLOW
        elif record.levelno == logging.INFO:
            level_color = Fore.BLUE
        else:
            level_color = Fore.GREEN
        
        log_fmt = f"{Fore.GREEN}{self.x_id}{Fore.WHITE}"
        log_fmt += f"%(asctime)s{Style.RESET_ALL}"
        log_fmt += f"{level_color} %(levelname)s {Style.RESET_ALL}%(message)s"

        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)



def get_logger(file_name: str) -> logging.Logger:
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
    return logger
