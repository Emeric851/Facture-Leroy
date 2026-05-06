import pandas as pd
from pathlib import Path

EXPORT_DIR = Path("downloads")

class CsvService:

    @staticmethod
    def export(data):

        if not data:
            return

        df = pd.DataFrame(data)

        path = EXPORT_DIR / "factures.csv"

        df.to_csv(path, index=False)

        return path
