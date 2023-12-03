import os
import logging

log_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
log_filename = os.path.join(log_dir, 'app.log')

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[
                        logging.FileHandler(log_filename),
                        logging.StreamHandler()
                    ]
                    )
