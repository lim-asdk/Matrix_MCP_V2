@echo off
set "PIP=c:\program_files\Lim Workspace\Matrix_MCP\.venv\Scripts\pip.exe"
"%PIP%" uninstall -y PySide6 pandas matplotlib yfinance shiboken6 PyQt6 PyQt6-Qt6 PyQt6-WebEngine matplotlib-inline qtpy PySide6-Essentials PySide6-Addons
"%PIP%" cache purge
