### Server ###

### 1. Generate and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Required Libraries
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
fastapi run src/main.py
```
- The server will run on http://0.0.0.0:8000

```bash
fastapi dev src/main.py
```
- The server will run on http://127.0.0.1:8000

### 4. API Endpoints
- **POST** /upload
  - **Request Body**
    - csv_file: File
  - **Response**
    - json
