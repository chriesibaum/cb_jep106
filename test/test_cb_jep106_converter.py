import pytest
import sys
import os
from cb_jep106_tools.cb_jep106_converter import main


class Test_cb_jep106_converter:

    def test_main_no_arguments(self, capsys):
        """Test that main() runs without arguments and uses default values."""
        with pytest.raises(SystemExit) as exc_info:
            sys.argv = ['cb_jep106_converter']
            main()

        assert exc_info.value.code == 2
        captured = capsys.readouterr()
        assert 'error' in captured.err
        assert 'at least one output option must be specified' in captured.err

    def test_help_option(self, capsys):
        """Test that -h prints usage information and exits with code 0."""
        with pytest.raises(SystemExit) as exc_info:
            sys.argv = ['cb_jep106_converter', '-h']
            main()

        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert 'usage:' in captured.out
        assert '--help' in captured.out
        assert '--pdf' in captured.out
        assert '--csv' in captured.out
        assert '--json' in captured.out

    def test_main_with_csv_output(self, capsys):
        """Test that main() runs with CSV output option."""
        sys.argv = ['cb_jep106_converter', '-c', 'test_output.csv']
        main()

        captured = capsys.readouterr()
        assert 'Writing JEP106 data to CSV file: test_output.csv' in captured.out

        # clean up generated file
        if os.path.exists('test_output.csv'):
            os.remove('test_output.csv')

    def test_main_with_json_output(self, capsys):
        """Test that main() runs with JSON output option."""
        sys.argv = ['cb_jep106_converter', '-j', 'test_output.json']
        main()

        captured = capsys.readouterr()
        assert 'Writing JEP106 data to JSON file: test_output.json' in captured.out

        # clean up generated file
        if os.path.exists('test_output.json'):
            os.remove('test_output.json')
