#!/usr/bin/env bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

BOLD='\033[1m'

function select_playbook() {
    local playbooks
    playbooks=$(find . -maxdepth 1 -type f -name "site-*.yml" -o -name "debug-*.yml" | sed 's|^\./||' | sort)

    # Check if any playbooks were found
    if [ -z "$playbooks" ]; then
        echo -e "${RED}${BOLD}Error:${NC} No playbook files found in the current directory."
        exit 1
    fi

    # Use gum to select a playbook
    local selected_playbook
    selected_playbook=$(echo "$playbooks" | gum choose  --header "Select a playbook to run:")

    echo "$selected_playbook"
}

function logCommand {
    local CMD="$1"
    local USAGE_DRY_RUN="${2:-false}"

    echo ""
    echo -e "🚀 ${GREEN}${BOLD}Executing:...${NC}"
    echo -e "   Command: ${BOLD}${CMD}${NC}"
    echo -e "   Working dir: ${BOLD}./${NC}"
    echo ""

    if [ "$usage_dry_run" == "true" ]; then
        echo -e "   💡 ${BOLD}Dry run enabled. Command not executed.${NC}"
        exit 0
    fi
}
