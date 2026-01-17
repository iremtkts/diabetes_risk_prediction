class DataLoaderError(Exception):

    pass

class InvalidFilePathError(DataLoaderError):
    pass

class FileNotFoundError(DataLoaderError):
    pass

class UnsupportedFileExtensionError(DataLoaderError):
    pass

class EmptyDataFileError(DataLoaderError):
    pass

class DataParsingError(DataLoaderError):
    pass

class UnexpectedDataLoaderError(DataLoaderError):
    pass