from src.config import DATA_FILE
from src.data_loader import DataLoader

loader = DataLoader()
df = loader.load_data(DATA_FILE)

print(df.head())