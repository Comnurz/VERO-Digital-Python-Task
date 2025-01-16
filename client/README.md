### Client ###

### 1. Generate and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 3. Run the Client
```bash
python client.py path/of/csv/file.csv -k <column_names> -c <boolean>
```
- path/of/csv/file.csv: Path of the CSV file
- -k/--keys: Column names to be used for generating xlsx file [optional]
- -c/--colored: Boolean value to check if the column needed to be colored or not [optional - default True]



