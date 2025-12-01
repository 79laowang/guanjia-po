# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

官家婆 (Guanjiapo) is a PyQt6-based personal finance and inventory management desktop application for Chinese users. It helps families manage income/expenses and track household inventory with statistical charts and reporting.

## Architecture

### High-Level Structure
- **MVC Pattern**: Clear separation between UI (View), Database (Model), and Business Logic
- **Modular Design**: Components organized in separate directories for maintainability
- **Local Storage**: All data stored locally in SQLite database (no cloud sync)
- **Single Application Instance**: Desktop application, not web-based

### Core Modules
1. **src/ui/** - All PyQt6 UI components and main window
2. **src/database/** - SQLite database management and ORM models
3. **src/widgets/** - Reusable custom PyQt6 widgets
4. **src/utils/** - Configuration, utilities, and helper functions

### Key Classes & Components
- **MainWindow** (src/ui/main_window.py:100+): Central application window with sidebar navigation
- **DatabaseManager** (src/database/database.py:8): SQLite connection and table management
- **Data Models** (src/database/models.py): Dataclasses for Category, Account, Item, InventoryTransaction
- **UI Pages**: DashboardWidget, AccountWidget, InventoryWidget, StatisticsWidget

### Database Schema
Four main tables:
- `categories` - Income/expense categories
- `accounts` - Individual income/expense records
- `item_categories` - Inventory item categories
- `items` - Inventory items with quantity tracking
- `inventory_transactions` - Stock in/out records

## Common Development Commands

### Running the Application
```bash
# Option 1: Using the helper script (recommended - auto-configures everything)
./run_app.sh

# Option 2: Manual setup with virtual environment
source guanjia_po_env/bin/activate
DISPLAY=:99 python run.py

# Option 3: System Python version (needs dependencies installed system-wide)
DISPLAY=:99 python3 run.py

# Text-based demo (no GUI required)
python3 text_demo.py

# Simple test version
python3 simple_test.py
```

### Installing Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Key dependencies (PyQt6, matplotlib, pandas, pillow, numpy)
pip install PyQt6==6.6.1 PyQt6-tools matplotlib pandas pillow numpy
```

### Building Executable
```bash
# Build standalone executable with PyInstaller
python build_exe.py

# Output: dist/官家婆.exe
```

### Testing
```bash
# Run simple test application
python simple_test.py
```

### Troubleshooting

**GUI requires display:**
```bash
# For headless environments, set DISPLAY
export DISPLAY=:99
# Or use the helper script which auto-configures this
./run_app.sh
```

**QStandardPaths error:**
```bash
export XDG_RUNTIME_DIR=/tmp
python run.py
```

**CSS Warning messages:**
You may see warnings like "Unknown property box-shadow" or "transform" when running the GUI. These are **harmless** - they occur because the QSS stylesheet includes web CSS properties that Qt doesn't support. The application works correctly despite these warnings.

**Using Virtual Environment:**
```bash
# Activate the pre-configured virtual environment
source guanjia_po_env/bin/activate
pip list  # Verify PyQt6 is installed

# Run the application
DISPLAY=:99 python run.py
```

## Configuration

### Application Configuration (src/utils/config.py)
- **Database Path**: `~/.guanjia-po/guanjia_po.db`
- **UI Colors**: Primary (#1890ff), Success (#52c41a), Error (#ff4d4f)
- **Font**: Microsoft YaHei, size 9
- **Default Categories**: Pre-configured income/expense categories
- **Theme**: Customizable via QSS stylesheets

### Development vs Production
- **Development**: Database stored in `APPLICATION_DIR/data/`
- **Frozen/Compiled**: Database stored in `~/.guanjia-po/`

## Important Files

### Entry Points
- `run.py` - Primary application launcher
- `src/main.py` - Main program entry point
- `run_system.py` - System Python launcher with error handling
- `run_app.sh` - Helper script to auto-configure environment and run the app

### Build & Setup
- `build_exe.py` - PyInstaller configuration for packaging
- `setup.py` - Python package metadata
- `requirements.txt` - Dependencies list

### UI Resources
- `resources/styles.qss` - QSS stylesheet for theming
- `resources/icons/` - Icon files (currently empty, needs population)

## Key Implementation Details

### Database Connection Pattern
```python
from src.database.database import DatabaseManager
db = DatabaseManager()  # Auto-initializes tables and connects
```

### Adding New Features
1. Create dataclass model in `src/database/models.py`
2. Add table creation SQL in `DatabaseManager.initialize_database()`
3. Create UI component in `src/ui/`
4. Add navigation button in `SidebarWidget` (src/ui/main_window.py:100+)
5. Register model defaults in `src/utils/config.py` if needed

### UI Styling
- Uses QSS (Qt Style Sheets) similar to CSS
- Colors defined in `COLORS` dict (src/utils/config.py:50)
- Custom button styles in `NavigationButton` (src/ui/main_window.py:17)

### Data Flow
1. UI Components → DatabaseManager → SQLite
2. Models are dataclasses with type hints
3. SQLite returns Row objects (dict-like access)
4. Database auto-initializes on first run

## Common Development Patterns

### Database Operations
```python
# Query example
cursor = self.connection.cursor()
cursor.execute("SELECT * FROM accounts WHERE type = ?", ('income',))
results = cursor.fetchall()
```

### Adding UI Components
```python
# In main_window.py
from .dashboard import DashboardWidget
from .account import AccountWidget

# In setup_ui()
self.pages['dashboard'] = DashboardWidget()
self.pages['account'] = AccountWidget()
```

### Working with Dates
- Database stores dates as `DATE` type
- Models use `datetime.date` from Python
- Format: 'YYYY-MM-DD'

## Missing Components & TODOs

The project appears complete in structure but may need:
- Icon files in `resources/icons/` (directory exists but empty)
- Full implementation of statistics charts (matplotlib integration)
- Data export/import functionality
- Category color picker UI
- Inventory transaction logging

## Technical Stack Summary

- **GUI Framework**: PyQt6
- **Database**: SQLite3 (built-in, no separate server)
- **Charts**: Matplotlib
- **Data Processing**: Pandas
- **Image Handling**: Pillow (PIL)
- **Numeric Operations**: NumPy
- **Packaging**: PyInstaller (Windows .exe)

## Notes

- Application is Chinese-language focused (UI text in Chinese)
- All dates use local timezone
- Database file is user-specific in home directory
- No authentication - single-user application
- No unit tests directory (use simple_test.py for verification)
- No git repository (.git not present)
