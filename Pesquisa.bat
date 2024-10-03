@echo off
cd C:\Users\lucas\PycharmProjects\pythonProject
pip install -r requirements.txt
cls
call .venv\Scripts\activate
python main.py
explorer C:\Users\lucas\PycharmProjects\pythonProject
pause