FMT_DIR="./"

python3 -m black ${FMT_DIR}
python3 -m isort ${FMT_DIR}
# python3 -m docformatter --in-place -r ${FMT_DIR} 
