# Usage

In an empty folder run
```bash
git clone https://github.com/FrosterIlia/Slicer.git
```
Then to create virtual environment, run

On Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On UNIX or Mac:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the program, run:
```bash
python main.py
```

To deactivate virtual environment, run
```bash
deactivate
```

## Pytest usage

To run the tests:
```bash
python -m pytest
```