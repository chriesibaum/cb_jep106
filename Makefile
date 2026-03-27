CB_JEP106_DIR := ./cb_jep106
CB_JEP106_TOOL_DIR := ./cb_jep106_tools
JEP106_DIR := ./JEP106
TEST_DIR := ./test


PYFILES := $(wildcard $(CB_JEP106_DIR)/*.py) \
		   $(wildcard $(CB_JEP106_TOOL_DIR)/*.py) \
 		   $(wildcard $(TEST_DIR)/*.py)

show_files:
	@echo "Python files to be checked:"
	@echo "$(PYFILES)"

BUILD_DIR := ./dist

# tools
E := @echo
PYCODESTYLE := pycodestyle
PYCODESTYLE_FLAGS := --show-source --show-pep8 --max-line-length=100 #--ignore=E501,E228,E722

AUTOPEP8 := autopep8
AUTOPEP8_FLAGS := --in-place --max-line-length=1000

FLAKE8 := flake8
FLAKE8_FLAGS := --show-source  --ignore=E501,E228,E722

BANDIT := bandit
BANDIT_FLAGS := --format custom --msg-template \
    "{abspath}:{line}: {test_id}[bandit]: {severity}: {msg}" \
	-c pyproject.toml


HATCH := hatch



all: doc

doc: badges


check: pycodestyle flake8 bandit

pycodestyle: $(patsubst %.py,%.pycodestyle,$(PYFILES))

%.pycodestyle:
	$(E) $(PYCODESTYLE) checking $*.py
	@$(AUTOPEP8) $(AUTOPEP8_FLAGS) $*.py
	@$(PYCODESTYLE) $(PYCODESTYLE_FLAGS) $*.py


flake8: $(patsubst %.py,%.flake8,$(PYFILES))

%.flake8:
	$(E) flake8 checking $*.py
	@$(FLAKE8) $(FLAKE8_FLAGS) $*.py


bandit: $(patsubst %.py,%.bandit,$(PYFILES))

%.bandit:
	$(E) bandit checking $*.py
	@$(BANDIT) $(BANDIT_FLAGS) $*.py




COV_RESULT:= ./reports/junit/junit.xml
COV_REPORT:= ./reports/coverage_html/index.html ./reports/coverage/coverage.xml
DOC_BADGES:= ./doc/tests-badge.svg ./doc/coverage-badge.svg

jep106_csv: $(JEP106_DIR)/jep106.csv
$(JEP106_DIR)/jep106.csv: $(JEP106_DIR)/JEP106BN.pdf
	$(E) Generating jep106.csv
	@python $(CB_JEP106_TOOL_DIR)/cb_jep106_converter.py \
	        -i $(JEP106_DIR)/JEP106BN.pdf -c $@


jep106_json: $(JEP106_DIR)/jep106.json
$(JEP106_DIR)/jep106.json: $(JEP106_DIR)/JEP106BN.pdf
	$(E) Generating jep106.json
	@python $(CB_JEP106_TOOL_DIR)/cb_jep106_converter.py \
	        -i $(JEP106_DIR)/JEP106BN.pdf -j $@

	cp $@ $(CB_JEP106_DIR)

test: $(COV_RESULT)
$(COV_RESULT): $(PYFILES) jep106_json
	coverage run  -m  \
		pytest -rP   --junit-xml=./reports/junit/junit.xml


cov_report: $(COV_REPORT)
$(COV_REPORT): $(COV_RESULT)
	coverage report -m
	coverage html -d ./reports/coverage_html
	coverage xml -o ./reports/coverage/coverage.xml


badges: $(DOC_BADGES)
$(DOC_BADGES): $(COV_RESULT) $(COV_REPORT)
	@echo "Generating coverage badge..."
	@genbadge tests --output-file ./doc/tests-badge.svg
	@genbadge coverage --output-file ./doc/coverage-badge.svg


build: jep106_json
	@$(E) Building the package...
	$(HATCH) build


install: build
	@$(E) Installing the package...
	@pip install dist/cb_jep106*.whl --force-reinstall


clean:
	@$(E) Cleaning up...
	@rm -f *.log *.log.*
	@rm -f ./bsdl_file_db/*.log  ./bsdl_file_db/*.log.*  ./test/bsdl_files/*.log  ./test/bsdl_files/*.log.*
	@rm -rf __pycache__
	@rm -rf */__pycache__
	@rm -rf ./$(BUILD_DIR)
	@rm -rf ./reports/
	@rm -f ./.coverage
	@rm -f $(JEP106_DIR)/jep106.csv
	@rm -f $(JEP106_DIR)/jep106.json


mr_proper: clean
	@$(E) Removing generated files...
	@rm -f $(CB_JEP106_DIR)/jep106.json
	@rm -f $(DOC_BADGES)
