from abc import ABC, abstractmethod
import pandas as pd
from .Database import MYSQLDataBase

class DataLoader(ABC):
    @abstractmethod
    def load(self):
        pass


class CSVLoader(DataLoader):
    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def load(self):
        print("Loading CSV file...")
        return pd.read_csv(self.filepath)


class JSONLoader(DataLoader):
    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def load(self):
        print("Loading CSV file...")
        return pd.read_json(self.filepath)


class DataLoaderFactory:
    def __init__(self, source: str, filepath: str):
        self.source: str = source
        self.filepath: str = filepath
        self.loader = None

    def create_loader(self):
        if self.source == "csv":
            self.loader = CSVLoader(filepath=self.filepath)
        elif self.source == "json":
            self.loader = JSONLoader(filepath=self.filepath)
        else:
            raise ValueError("Source not supported")
    
    def validate(self):
        self.create_loader()
        data = self.loader.load()
        columns = ['timestamp', 'sala', 'estado', 'temperatura', 'humedad', 'co2', 'mensaje']

        if list(data.columns) != columns:
            raise ValueError(f"ERROR: DataFrame must have exactly these columns: {columns}")
        
        return data



    
