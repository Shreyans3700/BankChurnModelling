import sys
import traceback
from src.logger import logging


def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed error message including file name, line number, and traceback.
    """
    _, _, exc_tb = error_detail.exc_info()

    # Traverse to the last traceback (actual error origin)
    while exc_tb and exc_tb.tb_next:
        exc_tb = exc_tb.tb_next

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
    else:
        file_name = "Unknown File"
        line_number = "Unknown Line"

    return (
        f"\nError occurred in script [{file_name}]"
        f"\nLine number [{line_number}]"
        f"\nError message [{str(error)}]"
        f"\n\nTraceback:\n{traceback.format_exc()}"
    )


class CustomException(Exception):
    def __init__(self, error_msg: Exception, error_detail: sys):
        """
        Custom Exception class for better debugging and logging.
        """
        self.error_msg = error_message_detail(error_msg, error_detail)

        # Log the error
        logging.error(self.error_msg)

        self.original_exception = error_msg

        super().__init__(self.error_msg)

    def __str__(self):
        return self.error_msg