# wordpress-extract
Extract data from various wordpress sites. Download images, text, and create spreadsheet according to defined body patterns

### Prerequisites
```shell
pip install -r requirements.txt
```

### Configuration
```
cp config.json.example config.json
```
Modify _body_patterns_ entries in config.json

##### body_patterns:
List of column names of the to-be created spreadsheet along with regexp which should extract required info from html body.

### Usage
The script takes list of URL as an argument. Example:
```shell
python zakaz_mebel.py url_list.txt
```