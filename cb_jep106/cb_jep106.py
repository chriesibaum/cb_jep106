import json
from pathlib import Path


def _default_db_path() -> Path:
    return Path(__file__).with_name('jep106.json')


class Jep106Db():
    """
    This class represents the CB_JEP106 package, which provides tools for working with JEP106 data.
    It loads the JEP106 data from a JSON file and provides methods to access the manufacturer
    information based on the JEDEC code.
    """

    def __init__(self, db_path: str | Path | None = None):
        self.json_path = Path(db_path) if db_path is not None else _default_db_path()

        self.jep106_data = self.load_jep106_json()

    def load_jep106_json(self):
        """Loads the JEP106 JSON file into a pandas DataFrame."""

        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Error: {self.json_path} not found. Please generate the JSON file first.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading the JSON file: {e}")

        # convert the data to a list of dictionaries for easier access
        # with key "11-bit-JEDEC-Code" for lookup
        data = {
            d["11-bit-JEDEC-Code"]: {
                'Bank': d['Bank'],
                'Index': d['Index'],
                'Manufacturer': d['Manufacturer'],
            }
            for d in json_data.values()
        }
        return data

    def get_manufacturer(self, jedec_code: int) -> str:
        try:
            return self.jep106_data[jedec_code]['Manufacturer']
        except KeyError as exc:
            raise ValueError("Manufacturer not found for the given JEDEC code.") from exc


# Example usage
def main():  # pragma: no cover
    jep106 = Jep106Db()
    print(jep106.get_manufacturer(0x001))
    print(jep106.get_manufacturer(0x020))
    print(jep106.get_manufacturer(0x23b))


if __name__ == "__main__":  # pragma: no cover
    main()
