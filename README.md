# NBA Dynamic Pricing Engine


*Dynamic pricing for NBA tickets, powered by Streamlit and real-time data.*

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Database Setup](#database-setup)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## Project Overview
The NBA Dynamic Pricing Engine is a Streamlit application that calculates real-time ticket prices for NBA games based on factors like team popularity, player performance, fan engagement, and game context (e.g., rivalries, national TV broadcasts). Built for the 2022-2023 NBA season, it uses historical game data from an SQLite database and provides an interactive UI for teams, platforms, and fans to optimize pricing.

**Purpose**: Maximize revenue while ensuring fair pricing.  
**Technologies**: Python, Streamlit, Pandas, SQLite, Requests, PIL, NumPy.

## Features
- **Interactive Pricing**: Select home/away teams, seat locations, and adjust factors (e.g., wins, star player impact) to get dynamic prices.
- **Price Breakdown**: View how factors (e.g., rivalry, injuries) affect the final price.
- **Historical Context**: Displays past games for the selected home team with estimated prices.
- **Export Reports**: Download pricing details as CSV.
- **Visual Appeal**: Team logos, responsive UI, and NBA-themed design.

## Installation
Follow these steps to set up and run the project locally.

### Prerequisites
- **Python**: Version 3.8 or higher ([Download](https://www.python.org/downloads/)).
- **Git**: Optional, for cloning the repository ([Download](https://git-scm.com/downloads)).
- **SQLite Database**: `nba.sqlite` from [Kaggle](https://www.kaggle.com/datasets/wyattowalsh/basketball).

### Steps
1. **Download the Repository**:
   - Click the green “Code” button and select “Download ZIP”.
   - Extract the ZIP file to a folder (e.g., `nba-dynamic-pricing`).
   - Alternatively, clone with Git:
     ```bash
     git clone https://github.com/yourusername/nba-dynamic-pricing.git
     cd nba-dynamic-pricing
     ```

2. **Install Dependencies**:
   - Open a terminal in the project folder.
   - Install requirements using the provided `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - This installs Streamlit, Pandas, Requests, Pillow, and NumPy.

3. **Download the Database**:
   - Download `nba.sqlite` from [Kaggle](https://www.kaggle.com/datasets/wyattowalsh/basketball).
   - Place it in `C:/Users/user/Projects/` (create the folder if needed).
   - Alternatively, update the database path in `nba_pricing_app.py` (see [Database Setup](#database-setup)).

4. **Verify Setup**:
   - Ensure `nba_pricing_app.py` and `requirements.txt` are in the project folder.
   - Confirm Python 3.8+ is installed (`python --version`).

## Usage
Run the application to explore dynamic pricing.

1. **Start the Application**:
   - In the terminal, navigate to the project folder:
     ```bash
     cd path/to/nba-dynamic-pricing
     ```
   - Run the app:
     ```bash
     streamlit run nba_pricing_app.py
     ```
   - The app opens in your browser (e.g., `http://localhost:8501`).

2. **Configure a Game**:
   - Select **Home Team** and **Away Team** from dropdowns (e.g., Lakers, Timberwolves).
   - Choose **Seat Location**: Upper Bowl ($50 base), Lower Bowl ($200), or Courtside ($500).
   - Adjust sliders/checkboxes:
     - **Home/Away Wins**: Wins in last 10 games (0–10).
     - **SPIF**: Star Player Impact Factor (0–50).
     - **FEC**: Fan Engagement Coefficient (0.5–1.5).
     - **Rivalry Game**: Check for rival matchups (+30%).
     - **National TV**: Check for televised games (+20%).
     - **Star Injured**: Check if a star is injured (-20%).

3. **View Results**:
   - See the **Recommended Ticket Price** (e.g., $1049 for Courtside).
   - Check the **Price Comparison** table for all seat locations.
   - Expand **Price Breakdown** for factor contributions (e.g., +20% for national TV).
   - View **Historical Examples** for past games (Upper Bowl estimates).
   - Download a **Price Report** as CSV.

**Example**:
- Lakers vs. Timberwolves, Courtside, 6 home wins, 4 away wins, SPIF=35, FEC=1.1, National TV, no rivalry/injuries:
  - Price: ~$1049 (base $500, adjusted for popularity, performance, etc.).

## Database Setup
The app uses `nba.sqlite` for historical game data.

1. **Download**:
   - Get `nba.sqlite` from [Kaggle](https://www.kaggle.com/datasets/wyattowalsh/basketball).

2. **Place the File**:
   - Default path: `C:/Users/user/Projects/nba.sqlite`.
   - Create the folder if it doesn’t exist.
   - To use a different path, set the `NBA_DB_PATH` environment variable or edit `nba_pricing_app.py`:
     ```python
     os.environ['NBA_DB_PATH'] = '/path/to/your/nba.sqlite'
     ```

3. **Verify Schema**:
   - The database must contain `game` and `team` tables.
   - Use a tool like [DB Browser for SQLite](https://sqlitebrowser.org/) to check.
   - The app queries 2022 games using team nicknames.

4. **Permissions**:
   - Ensure the file is readable:
     - Windows: Right-click `nba.sqlite` > Properties > Security > Grant Read permissions to your user.
     - macOS/Linux: Run `chmod +r nba.sqlite`.

## Troubleshooting
- **Database Errors**:
  - *“Database file not found”*: Verify `nba.sqlite` is in `C:/Users/user/Projects/` or update `NBA_DB_PATH`.
  - *“Permission denied”*: Check file permissions (see [Database Setup](#database-setup)).
  - *“No ‘game’ table”*: Download the correct `nba.sqlite` from Kaggle.
- **Dependency Issues**:
  - Re-run `pip install -r requirements.txt`.
  - Ensure Python 3.8+ (`python --version`) and compatible library versions.
  - Use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
- **Logo Loading**:
  - If team logos fail, check internet connectivity (logos are fetched from NBA CDN).
- **Streamlit Errors**:
  - Update Streamlit: `pip install --upgrade streamlit`.
  - Restart the app: `streamlit run nba_pricing_app.py`.
  - Check for port conflicts (default: 8501).

For further help, open an [Issue](https://github.com/LoChunHangMax/nba-dynamic-pricing/issues) on this repository.
