import os
import pandas as pd

class DataBasePandas:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.file_path = f'database/{self.table_name}.csv'
        self.columns = columns
        self.init_database()

    def init_database(self):
        os.makedirs('database', exist_ok=True)
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.file_path, index=False)

    def get_table(self):
        return pd.read_csv(self.file_path)

    def inserir_dados(self, data):
        new_data = pd.DataFrame(data, columns=self.columns)
        database = self.get_table()
        database = pd.concat([database, new_data], ignore_index=True)
        database.to_csv(self.file_path, index=False)
