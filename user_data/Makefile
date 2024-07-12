# Specify the name of the Python script to be run by the "make" or "make run" command.
SCRIPT=run_fast_baseline.py
#run_fast_experiment_1.py

# Custom variable definitions that determine which model is run or tested
VERSION=2R
BUILD=179

# The date and time stamp for the current run
DATE_STAMP := $(shell date +"%Y-%m-%d %H:%M:%S")

# SYSTEM CONFIGURATION
SYM=sym

# Identify the model being run or tested
MODEL=$(VERSION)_$(BUILD)

# (default target) Run the chosen target by default
default: run

# Basic example of running a script
run:
	python3 $(VERSION)/$(BUILD)/python/$(SCRIPT)

charts:
	python3 -m gcubed.graphics.hypercube

# Target to add changes, commit, and push
push:
	@read -p "Enter commit message: " message; \
	echo "Adding changes..."; \
	git add .; \
	echo "Committing changes..."; \
	git commit -m "$$message"; \
	echo "Pushing to remote repository..."; \
	git push; \
	echo "Done"

# Eventually we should also support https://www.redswitches.com/blog/squash-commits/

commit:
	@read -p "Enter commit message: " message; \
	echo "Adding changes..."; \
	git add .; \
	echo "Committing changes..."; \
	git commit -m "$$message"; \
	echo "Done"

# Add a note to a branch to describe it
desc:
	@read -p "Enter branch description: " description; \
	echo "Adding branch description..."; \
	git notes add -f -m "BRANCH_DESCRIPTION $(DATE_STAMP): $$description"; \
	echo "Done"

# Show the description of a branch
show:
	git notes show

# Run the SYM processor
sym:
	@echo "Running SYM processor for model $(VERSION) build $(BUILD) ..." ; \
	cd $(VERSION) && cd $(BUILD) && cd sym ;\
	rm -f *.html && rm -f *.csv && rm -f *.lis && rm -f *.py ;\
	pwd ; \
	$(SYM) -html   ggg-$(VERSION)-$(BUILD).sym model_$(VERSION)_$(BUILD).html ;\
	$(SYM) -python ggg-$(VERSION)-$(BUILD).sym model_$(VERSION)_$(BUILD).py ;\
	ls -la ;\
	cd ..  && cd .. && cd .. ;\
	echo "... Done" ;


# Remove temporary python files
clean:
	rm -rf *.pyc
	rm -rf *.pyd
	rm -rf *.py0
	
delete_results:
	find results -mindepth 1 -type d -exec rm -rf {} \;

# List the targets that are not related to specific file timestamps
.PHONY: run, charts, push, commit, desc, show, sym, clean, delete_results
