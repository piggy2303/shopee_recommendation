FILE=data.zip
if [ ! -f "$FILE" ]; then
    echo "$FILE not found"
    python3 download_data.py
fi
echo "Download complete"

FILE=data
if [ ! -d "$FILE" ]; then
    echo "$FILE not found"
    unzip data.zip -d data
fi

echo "unzip complete"


python3 crawl_data.py
python3 cleaning_preprocesing.py
python3 recommendation.py