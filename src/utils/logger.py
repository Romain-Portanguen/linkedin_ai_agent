import logging
from typing import Optional

def setup_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger with standardised parameters.
    
    Args:
        name: Logger name (uses root logger if None)
        level: Logging level (INFO by default)
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger('linkedin_agent') 