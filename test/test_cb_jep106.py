import pytest

from cb_jep106 import cb_jep106


def get_test_params():
    return [
        (0x001, "AMD"),
        (0x020, "STMicroelectronics"),
        (0x23b, "ARM Ltd"),
    ]


class TestCB_JEP106:
    @pytest.fixture(autouse=True, params=get_test_params())
    @classmethod
    def setup_class(self, request):
        self.jep106db = cb_jep106.Jep106Db()

        self.jedec_code, self.expected_manufacturer = request.param

    def test_get_manufacturer(self):
        manufacturer = self.jep106db.get_manufacturer(self.jedec_code)
        assert manufacturer == self.expected_manufacturer

    def test_manufacturer_code_type(self):
        manufacturer = self.jep106db.get_manufacturer(self.jedec_code)
        assert isinstance(manufacturer, str)


class TestCB_JEP106Errors:
    def setup_class(self):
        self.jep106db = cb_jep106.Jep106Db()

    def test_get_manufacturer_not_found(self):
        with pytest.raises(ValueError,
                           match="Manufacturer not found for the given JEDEC code."):
            self.jep106db.get_manufacturer(0x999)


class TestCB_JEP106DataLoading:
    def test_load_jep106_json_file_not_found(self, monkeypatch):
        def fake_open(*args, **kwargs):
            raise FileNotFoundError("File not found")

        monkeypatch.setattr("builtins.open", fake_open)

        with pytest.raises(FileNotFoundError,
                           match="Error: .* not found. Please generate the JSON file first."):
            cb_jep106.Jep106Db()

    def test_load_jep106_json_invalid_format(self, monkeypatch):
        def fake_open(*args, **kwargs):
            from io import StringIO
            return StringIO("invalid json")

        monkeypatch.setattr("builtins.open", fake_open)

        with pytest.raises(RuntimeError,
                           match="An error occurred while loading the JSON file: .*"):
            cb_jep106.Jep106Db()
