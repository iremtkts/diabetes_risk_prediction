import os
from pathlib import Path
import logging
import pandas as pd
from typing import Optional, Union


from .error_messages import (
    DataReadingErrorMessages as EM,
    SUPPORTED_FILE_EXTENSIONS,
)
from .exceptions import (
    InvalidFilePathError,
    FileNotFoundError as DataFileNotFoundError,
    UnsupportedFileExtensionError,
    EmptyDataFileError,
    DataParsingError,
    UnexpectedDataLoaderError,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


data_reader_functions = {
    ".csv": pd.read_csv,
    ".parquet": pd.read_parquet
}


class DataLoader:
  
    
    def load_data(self, file_path: Union[str, Path]) -> Optional[pd.DataFrame]:
        
        try:
            
            self._validate_file_path(file_path)
            
            
            ext = self._check_if_file_extension_supported(file_path)
            
           
            reader_func = data_reader_functions.get(ext)
            
            
            data: pd.DataFrame = reader_func(file_path)
            
           
            if data.empty:
                logger.error(EM.EMPTY_DATA_FILE.value)
                raise EmptyDataFileError(EM.EMPTY_DATA_FILE.value)
            
            logger.info(f"Data loaded successfully from {file_path}")
            return data
            
        except (InvalidFilePathError, DataFileNotFoundError, 
                UnsupportedFileExtensionError, EmptyDataFileError,
                DataParsingError):
            
            raise
        except Exception as e:
         
            logger.error(EM.UNEXPECTED_ERROR.value.format(error=str(e)))
            raise UnexpectedDataLoaderError(
                EM.UNEXPECTED_ERROR.value.format(error=str(e))
            ) from e
    
    def _validate_file_path(self, file_path: Union[str, Path]) -> None:
        
      
        if not isinstance(file_path, (str, Path)):
            error_msg = EM.INVALID_FILE_PATH_TYPE.value.format(
                type=type(file_path).__name__
            )
            logger.error(error_msg)
            raise InvalidFilePathError(error_msg)
        
       
        if not os.path.exists(file_path):
            error_msg = EM.FILE_NOT_FOUND.value.format(file_path=file_path)
            logger.error(error_msg)
            raise DataFileNotFoundError(error_msg)
    
    def _check_if_file_extension_supported(
        self, file_path: Union[str, Path]
    ) -> str:
        
        ext = Path(file_path).suffix
        
        if ext not in SUPPORTED_FILE_EXTENSIONS:
            error_msg = EM.EXT_NOT_SUPPORTED.value.format(
                ext=ext,
                supported_extensions=SUPPORTED_FILE_EXTENSIONS
            )
            logger.error(error_msg)
            raise UnsupportedFileExtensionError(error_msg)
        
        return ext