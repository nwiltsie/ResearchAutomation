#!/bin/bash

# Function to print colored text
color_echo() {
    local color=$1
    shift
    local message="$*"

    # Color codes
    case $color in
        black) color_code="\033[0;30m" ;;
        red) color_code="\033[0;31m" ;;
        green) color_code="\033[0;32m" ;;
        yellow) color_code="\033[0;33m" ;;
        blue) color_code="\033[0;34m" ;;
        magenta) color_code="\033[0;35m" ;;
        cyan) color_code="\033[0;36m" ;;
        white) color_code="\033[0;37m" ;;
        reset) color_code="\033[0m" ;; # Reset to default color
        *) echo "Invalid color: $color"; return 1 ;;
    esac

    # Print the message with the selected color
    echo -e "${color_code}${message}\033[0m"
}

# Initialize conda
color_echo green "Initializing conda..."

# This might need to be adjusted for other configurations
if [ -f "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
    # shellcheck source=/dev/null
    . "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh"
fi

ENV_NAME="unstable_test"

# Test if the environment already exists
if conda list --name $ENV_NAME > /dev/null 2>&1; then
    color_echo red "An environment named '$ENV_NAME' already exists."
    color_echo red "Manually remove it or change the variable name in the script."
    color_echo yellow "Command: conda env remove --name $ENV_NAME"
    exit 1
fi

# Create a conda environment with tensorflow
color_echo green "Creating conda environment..."
conda create \
    --name $ENV_NAME \
    --yes \
    --quiet \
    tensorflow

# Activate the environment
color_echo green "Activating the environment..."
conda activate $ENV_NAME

# Check that tensorflow is working
color_echo green "Confirming tensorflow is working..."
(python3 -c "import tensorflow" && color_echo yellow "Clean tensorflow works!") || \
    color_echo red "Clean tensorflow didn't work!"

# Install matplotlib with pip
color_echo green "Installing matplotlib using pip..."
python3 -m pip install \
    --no-input \
    --quiet \
    matplotlib

# Confirm that tensorflow is broken
color_echo green "Checking tensorflow again..."
(python3 -c "import tensorflow" && color_echo yellow "Modified tensorflow works!") || \
    color_echo red "Tensorflow failed in modified environment!"

color_echo green "Cleaning up the environment..."
conda deactivate
conda env remove --yes --name $ENV_NAME

color_echo green "Environment removed"
