#! /bin/bash

# CONFIG:

CONFIG_FILE="config.ini"
DataPath=$(grep '^DataPath' "$CONFIG_FILE" | cut -d'=' -f2)
echo "Data path is: $DataPath"


DATA_PATH=$DataPath
REPO_PATH=$(pwd)
echo "Using DATA_PATH=$DATA_PATH"

# Create local python virtual environment
echo "Creating virtual environment 'muons_workbook-venv'"
python3 -m venv muons_workbook-venv

source muons_workbook-venv/bin/activate

# Install dependencies from requirements.txt file
echo "Installing python dependencies"
pip3 install -r requirements.txt

# Build local file structure
echo "Building local file structure"
mkdir -p lcd plots out


bintocsv () {
    RUN_PATH=$REPO_PATH/lcd/Run$1
    mkdir -p $RUN_PATH
    for ((i=1; i<=$2; i++)); do
        cp $DATA_PATH/Run$1/meta.json $RUN_PATH
        python scripts/bintocsv.py $DATA_PATH/Run$1/scope-$i.bin $RUN_PATH
    done
    }

echo "Starting conversions of waveforms from raw binary to csv int /lcd directory"

for ((j=0; j<17; j++)); do
    echo "Converting Run$j"
    bintocsv $j "2"
done

for ((j=17; j<31; j++)); do
    bintocsv $j "1"
    echo "Converting Run$j"
done

echo "Done."