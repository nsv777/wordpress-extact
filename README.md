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

##### url_list.txt:
List of urls to parse.

##### body_patterns:
List of column names of the to-be created spreadsheet along with regexp which should extract required info from html body.

