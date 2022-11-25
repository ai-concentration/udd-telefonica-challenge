import os
import json

from abc import ABC, abstractmethod

from .constants import DATA_DIR
from .constants import JSON_DIR


class DataStorer(ABC):
    def __init__(self, file_name):
        self.file_name = file_name

    @abstractmethod
    def store(self):
        pass

    def verify_target(self, target):
        try:
            os.mkdir(DATA_DIR)
        except FileExistsError:
            print("Directory already exists")
        except:
            raise Exception("Directory could not be created")
            

class CSVStorer(DataStorer):
    def __init__(self, file_name, df):
        super().__init__(file_name)
        self.df = df

    def store(self):
        self.verify_target(DATA_DIR)

        self.df.to_csv(
            path_or_buf=DATA_DIR / f"{self.file_name}.csv",
            index=False
        )

        
class JSONStorer(DataStorer):
    def __init__(self, file_name, json_dict):
       super().__init__(file_name)
       self.json_dict = json_dict

    def store(self):
        self.verify_target(JSON_DIR)

        with open(JSON_DIR / f"{self.file_name}.json", "w") as f:
            json.dump(self.json_dict, f)


if __name__ == "__main__":
    pass