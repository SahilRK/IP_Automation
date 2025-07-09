import logging
from datetime import date

def create_log_file():
    #Create a logger and configure the log location
    log_file_name = date.strftime(date.today(),'%d_%m_%Y')
    logging.basicConfig(filename=f"./logs/ExecutionLog_{log_file_name}.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
    logger =  logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    return logger

logger = create_log_file()