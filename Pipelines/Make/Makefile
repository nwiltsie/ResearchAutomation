.DEFAULT_GOAL := all

OUTPUT_DIR := output
TEMP_DIR := temp

$(OUTPUT_DIR):
	@mkdir -p $@

$(TEMP_DIR):
	@mkdir -p $@

# Define the CSV file
CSV_FILE := ../data/2021-02-18-data.csv

# Extract IDs from the CSV
IDS := $(shell ../scripts/print_racer_names.py $(CSV_FILE))

RAW_RACER_DATAFILES := $(patsubst %, $(TEMP_DIR)/raw-%.json, $(IDS))
CLEAN_RACER_DATAFILES := $(patsubst %, $(TEMP_DIR)/clean-%.json, $(IDS))
RACER_LAP_PLOTS := $(patsubst %, $(OUTPUT_DIR)/lap-%.png, $(IDS))
RACER_SPLIT_PLOTS := $(patsubst %, $(OUTPUT_DIR)/split-%.png, $(IDS))

debug:
	@$(info IDS = $(IDS))
	@$(info RACER_DATAFILES = $(RACER_DATAFILES))

# Define the rule for extracting a single racer's data
EXTRACT_SCRIPT := ../scripts/extract_racer_data.py
$(TEMP_DIR)/raw-%.json: $(CSV_FILE) $(EXTRACT_SCRIPT) | $(TEMP_DIR)
	$(EXTRACT_SCRIPT) "$<" --name "$*" "$@"

# Define the rule for cleaning a single racer's data
CLEAN_SCRIPT := ../scripts/clean_racer_data.py
$(TEMP_DIR)/clean-%.json: $(TEMP_DIR)/raw-%.json $(CLEAN_SCRIPT) | $(TEMP_DIR)
	$(CLEAN_SCRIPT) "$<" "$@"

# Define the rule for plotting a single racer's data
PLOT_SCRIPT := ../scripts/plot_data.py
$(OUTPUT_DIR)/lap-%.png: $(TEMP_DIR)/clean-%.json $(PLOT_SCRIPT) | $(OUTPUT_DIR)
	$(PLOT_SCRIPT) "$<" "$@" --type lap

$(OUTPUT_DIR)/split-%.png: $(TEMP_DIR)/clean-%.json $(PLOT_SCRIPT) | $(OUTPUT_DIR)
	$(PLOT_SCRIPT) "$<" "$@" --type split

# Define the rule for re-merging all of the racer data
MERGED_DATA := $(TEMP_DIR)/merged.json
MERGE_SCRIPT := ../scripts/merge_racer_data.py
$(MERGED_DATA): $(CLEAN_RACER_DATAFILES) $(MERGE_SCRIPT) | $(TEMP_DIR)
	$(MERGE_SCRIPT) "$@" $(CLEAN_RACER_DATAFILES)

# Define the rule for plotting the re-merged data
MERGED_LAP_PLOT := $(OUTPUT_DIR)/merged-lines.png
MERGED_SPLIT_PLOT := $(OUTPUT_DIR)/merged-split.png

$(MERGED_LAP_PLOT): $(MERGED_DATA) $(PLOT_SCRIPT) | $(OUTPUT_DIR)
	$(PLOT_SCRIPT) "$<" "$@" --type lap

$(MERGED_SPLIT_PLOT): $(MERGED_DATA) $(PLOT_SCRIPT) | $(OUTPUT_DIR)
	$(PLOT_SCRIPT) "$<" "$@" --type split

all: $(MERGED_LAP_PLOT) $(MERGED_SPLIT_PLOT) $(RACER_LAP_PLOTS) $(RACER_SPLIT_PLOTS)

clean:
	@echo "Cleaning up..."
	@rm -rf $(OUTPUT_DIR) $(TEMP_DIR)

.PHONY: all clean
