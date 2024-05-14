#################################################################################
# GLOBALS                                                                       #
#################################################################################
SHELL := /bin/bash
PACKAGE_DIR = src
PYTHON_INTERPRETER = $(or poetry run python, $(shell which python3), $(shell which python))
STREAMLIT_PORT = 8501

#################################################################################
# TERMINAL COLORS                                                               #
#################################################################################
# Terminal Colors:
# to see all colors, run
# bash -c 'for c in {0..255}; do tput setaf $c; tput setaf $c | cat -v; echo =$c; done'
# the first 15 entries are the 8-bit colors

# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BOLD         := $(shell tput -Txterm bold)
	UNDERLINE    := $(shell tput -Txterm smul)
	STANDOUT     := $(shell tput -Txterm smso)
	BLACK        := $(shell tput -Txterm setaf 0)
	RED          := $(shell tput -Txterm setaf 1)
	GREEN        := $(shell tput -Txterm setaf 2)
	YELLOW       := $(shell tput -Txterm setaf 3)
	BLUE         := $(shell tput -Txterm setaf 4)
	PURPLE       := $(shell tput -Txterm setaf 5)
	CYAN         := $(shell tput -Txterm setaf 6)
	WHITE        := $(shell tput -Txterm setaf 7)
	NORMAL := $(shell tput -Txterm sgr0)
else
	BOLD         := ""
	UNDERLINE    := ""
	STANDOUT     := ""
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	BLUE         := ""
	PURPLE       := ""
	CYAN         := ""
	WHITE        := ""
	NORMAL       := ""
endif


##############################################################################
# Makefile TARGETS                                                           #
##############################################################################

.PHONY: helper-line help install git-init install-full install-dev clean-tmp-files build format lint full_check tests serve-docs
.DEFAULT_GOAL := help

##############################################################################
# MAKEFILE HELP                                                              #
##############################################################################

helper-line:
	@echo "${BOLD}${BLUE}--------------------------------------------------${NORMAL}"

help: ## Affiche la documentation
	@make --no-print-directory helper-line
	@echo "${BOLD}${BLUE}Here are all the targets available with make command.${NORMAL}"
	@make --no-print-directory helper-line
	@echo ""
	@echo "Start by running ${YELLOW}'make clean install'${NORMAL}"
	@echo ""
	@grep -E '^[a-zA-Z_0-9%-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "    ${YELLOW}%-30s${NORMAL} %s\n", $$1, $$2}'


#################################################################################
# INSTALLATION COMMANDS                                                         #
#################################################################################

install: install-full git-init pre-commit-init  ## >>> MAIN TARGET. Run this to start. <<<

install-full: ## Installe le projet en mode editable
	@echo ""
	@echo "${YELLOW}Install dependencies and creating virtual env with poetry${NORMAL}"
	@make --no-print-directory helper-line
	poetry install

git-init: ## Init the git project with init branch named main
	@echo "${YELLOW}Initializing git repository.${NORMAL}"
	git init --initial-branch=main

pre-commit-init:
	@echo "${GREEN}Initializing pre-commit hooks.${NORMAL}"
	pre-commit install

install-dev: ## Install les dépendances de développement
	@echo ""
	@echo "${ORANGE}Installing Dev dependencies.${NORMAL}"
	@make --no-print-directory helper-line
	poetry install --with dev

clean-tmp-files: ## Supprime les fichiers temporaires de compilation
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


# #################################################################################
# # BUILD COMMAND                                                                 #
# #################################################################################
build: ## Build le package
	@echo ""
	@echo "${YELLOW}Building the project:${NORMAL}"
	@make --no-print-directory helper-line
	rm -rf dist/*
	rm -rf build/*
	poetry build

# #################################################################################
# # QUALITY CHECK COMMANDS                                                        #
# #################################################################################

lint:  ## Lance le linter ruff
	@echo ""
	@echo "${YELLOW}Ruff linter Analysis:${NORMAL}"
	@make --no-print-directory helper-line
	poetry run ruff check --diff ${PACKAGE_DIR}


format: ## Lance le formattage des fichiers python avec Ruff
	@echo "${YELLOW}Start formatting with ruff:${NORMAL}"
	poetry run ruff format ${PACKAGE_DIR}


full_check: ## Lance le formattage, le linting avec ruff et le check mypy
	@echo ""
	@make format
	@echo ""
	@make lint
	@echo ""
	@echo "${YELLOW}Start static typing analysis with mypy:${NORMAL}"
	poetry run mypy ${PACKAGE_DIR}


#################################################################################
# DOCUMENTATION COMMANDS                                                        #
#################################################################################

mkdocs_installed: ## Vérifie l'installation de mkdocs dans l'environnement
	@echo ""
	@echo "${YELLOW}Verification si le package mkdocs est installé...${NORMAL}"
	@make --no-print-directory helper-line
	@if ! ${PYTHON_INTERPRETER} -c 'import mkdocs;' &> /dev/null; then \
		echo "${YELLOW}mkdocs non installé.${NORMAL}"; \
		exit 1; \
	fi

serve-docs: mkdocs_installed ## Génère la documentation
	poetry run mkdocs serve


#################################################################################
# STREAMLIT COMMANDS                                                        #
#################################################################################

streamlit_installed: ## Vérifie l'installation de streamlit dans l'environnement
	@echo ""
	@echo "${YELLOW}Verification si le package streamlit est installé...${NORMAL}"
	@make --no-print-directory helper-line
	@if ! ${PYTHON_INTERPRETER} -c 'import streamlit;' &> /dev/null; then \
		echo "${YELLOW}streamlit non installé.${NORMAL}"; \
		exit 1; \
	fi
# TODO : Remove all docker related stuff
streamlit_build: streamlit_installed  ## Construit l'image docker pour l'application streamlit
	$(eval PROJECT_NAME = $(shell ${PYTHON_INTERPRETER} -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["name"])'))
	docker build --build-arg HTTP_PROXY=${http_proxy} --build-arg HTTPS_PROXY=${https_proxy} -t ${PROJECT_NAME}-streamlit .

streamlit_run: streamlit_installed  ## Construit l'image docker pour l'application streamlit
	$(eval PROJECT_NAME = $(shell ${PYTHON_INTERPRETER} -c 'import toml; print(toml.load("pyproject.toml")["tool"]["poetry"]["name"])'))
	docker run --rm -it -p ${STREAMLIT_PORT}:${STREAMLIT_PORT} -v "$(shell pwd):/app" ${PROJECT_NAME}-streamlit
