# Sellerboard upload COGS

## Overview

Use selenium to automatically upload COGS to sellerboard by batch.

## Preparation

You need to create a `.env` file in the root directory of the project that contains your sellerboard credentials. For example:
```
EMAIL=admin@admin.com
PASSWORD=password
```

## Procedure

### 1. Setup environment

For Windows:
```bash
python -m venv .venv
.venv/Scripts/activate
```

For Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install required packages:
```bash
pip install -r requirements
```

### 2. Run project

```bash
python src/main.py
```

## Issues

- This project is a demo to upload COGS locally in host computer.
