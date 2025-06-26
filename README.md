# athross
Awesome Tracker Open Source System

Create and activate virtual environment:

```
python3 -m venv .venv
pip3 install -r build/requirements.txt
.\.venv\Scripts\Activate.ps1
```

To execute tests:
```
PYTHONPATH=. pytest tests/ --asyncio-mode=auto
```
```
$env:PYTHONPATH="."; pytest tests/ --asyncio-mode=auto
```
