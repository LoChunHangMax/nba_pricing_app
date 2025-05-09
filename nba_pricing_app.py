import streamlit as st
import pandas as pd
import sqlite3
import requests
from PIL import Image
import io
import numpy as np
from datetime import datetime
import os

# ================== NBA Data Structures ==================
TEAM_DATA = {
    "Atlanta Hawks": {
        "arena": "State Farm Arena",
        "popularity": 6.2,
        "nickname": "Hawks",
        "logo": "https://cdn.nba.com/logos/nba/1610612737/primary/L/logo.svg"
    },
    "Boston Celtics": {
        "arena": "TD Garden",
        "popularity": 8.7,
        "nickname": "Celtics",
        "logo": "https://cdn.nba.com/logos/nba/1610612738/primary/L/logo.svg"
    },
    "Brooklyn Nets": {
        "arena": "Barclays Center",
        "popularity": 7.8,
        "nickname": "Nets",
        "logo": "https://cdn.nba.com/logos/nba/1610612751/primary/L/logo.svg"
    },
    "Charlotte Hornets": {
        "arena": "Spectrum Center",
        "popularity": 5.9,
        "nickname": "Hornets",
        "logo": "https://cdn.nba.com/logos/nba/1610612766/primary/L/logo.svg"
    },
    "Chicago Bulls": {
        "arena": "United Center",
        "popularity": 8.3,
        "nickname": "Bulls",
        "logo": "https://cdn.nba.com/logos/nba/1610612741/primary/L/logo.svg"
    },
    "Cleveland Cavaliers": {
        "arena": "Rocket Mortgage FieldHouse",
        "popularity": 6.8,
        "nickname": "Cavaliers",
        "logo": "https://cdn.nba.com/logos/nba/1610612739/primary/L/logo.svg"
    },
    "Dallas Mavericks": {
        "arena": "American Airlines Center",
        "popularity": 7.5,
        "nickname": "Mavericks",
        "logo": "https://cdn.nba.com/logos/nba/1610612742/primary/L/logo.svg"
    },
    "Denver Nuggets": {
        "arena": "Ball Arena",
        "popularity": 7.2,
        "nickname": "Nuggets",
        "logo": "https://cdn.nba.com/logos/nba/1610612743/primary/L/logo.svg"
    },
    "Detroit Pistons": {
        "arena": "Little Caesars Arena",
        "popularity": 6.0,
        "nickname": "Pistons",
        "logo": "https://cdn.nba.com/logos/nba/1610612765/primary/L/logo.svg"
    },
    "Golden State Warriors": {
        "arena": "Chase Center",
        "popularity": 9.5,
        "nickname": "Warriors",
        "logo": "https://cdn.nba.com/logos/nba/1610612744/primary/L/logo.svg"
    },
    "Houston Rockets": {
        "arena": "Toyota Center",
        "popularity": 6.7,
        "nickname": "Rockets",
        "logo": "https://cdn.nba.com/logos/nba/1610612745/primary/L/logo.svg"
    },
    "Indiana Pacers": {
        "arena": "Gainbridge Fieldhouse",
        "popularity": 6.1,
        "nickname": "Pacers",
        "logo": "https://cdn.nba.com/logos/nba/1610612754/primary/L/logo.svg"
    },
    "LA Clippers": {
        "arena": "Intuit Dome",
        "popularity": 7.0,
        "nickname": "Clippers",
        "logo": "https://cdn.nba.com/logos/nba/1610612746/primary/L/logo.svg"
    },
    "Los Angeles Lakers": {
        "arena": "Crypto.com Arena",
        "popularity": 9.8,
        "nickname": "Lakers",
        "logo": "https://cdn.nba.com/logos/nba/1610612747/primary/L/logo.svg"
    },
    "Memphis Grizzlies": {
        "arena": "FedExForum",
        "popularity": 6.5,
        "nickname": "Grizzlies",
        "logo": "https://cdn.nba.com/logos/nba/1610612763/primary/L/logo.svg"
    },
    "Miami Heat": {
        "arena": "Kaseya Center",
        "popularity": 8.0,
        "nickname": "Heat",
        "logo": "https://cdn.nba.com/logos/nba/1610612748/primary/L/logo.svg"
    },
    "Milwaukee Bucks": {
        "arena": "Fiserv Forum",
        "popularity": 7.7,
        "nickname": "Bucks",
        "logo": "https://cdn.nba.com/logos/nba/1610612749/primary/L/logo.svg"
    },
    "Minnesota Timberwolves": {
        "arena": "Target Center",
        "popularity": 6.4,
        "nickname": "Timberwolves",
        "logo": "https://cdn.nba.com/logos/nba/1610612750/primary/L/logo.svg"
    },
    "New Orleans Pelicans": {
        "arena": "Smoothie King Center",
        "popularity": 6.3,
        "nickname": "Pelicans",
        "logo": "https://cdn.nba.com/logos/nba/1610612740/primary/L/logo.svg"
    },
    "New York Knicks": {
        "arena": "Madison Square Garden",
        "popularity": 8.9,
        "nickname": "Knicks",
        "logo": "https://cdn.nba.com/logos/nba/1610612752/primary/L/logo.svg"
    },
    "Oklahoma City Thunder": {
        "arena": "Paycom Center",
        "popularity": 6.6,
        "nickname": "Thunder",
        "logo": "https://cdn.nba.com/logos/nba/1610612760/primary/L/logo.svg"
    },
    "Orlando Magic": {
        "arena": "Kia Center",
        "popularity": 6.2,
        "nickname": "Magic",
        "logo": "https://cdn.nba.com/logos/nba/1610612753/primary/L/logo.svg"
    },
    "Philadelphia 76ers": {
        "arena": "Wells Fargo Center",
        "popularity": 8.1,
        "nickname": "76ers",
        "logo": "https://cdn.nba.com/logos/nba/1610612755/primary/L/logo.svg"
    },
    "Phoenix Suns": {
        "arena": "Footprint Center",
        "popularity": 7.4,
        "nickname": "Suns",
        "logo": "https://cdn.nba.com/logos/nba/1610612756/primary/L/logo.svg"
    },
    "Portland Trail Blazers": {
        "arena": "Moda Center",
        "popularity": 6.5,
        "nickname": "Trail Blazers",
        "logo": "https://cdn.nba.com/logos/nba/1610612757/primary/L/logo.svg"
    },
    "Sacramento Kings": {
        "arena": "Golden 1 Center",
        "popularity": 6.3,
        "nickname": "Kings",
        "logo": "https://cdn.nba.com/logos/nba/1610612758/primary/L/logo.svg"
    },
    "San Antonio Spurs": {
        "arena": "Frost Bank Center",
        "popularity": 6.8,
        "nickname": "Spurs",
        "logo": "https://cdn.nba.com/logos/nba/1610612759/primary/L/logo.svg"
    },
    "Toronto Raptors": {
        "arena": "Scotiabank Arena",
        "popularity": 7.6,
        "nickname": "Raptors",
        "logo": "https://cdn.nba.com/logos/nba/1610612761/primary/L/logo.svg"
    },
    "Utah Jazz": {
        "arena": "Delta Center",
        "popularity": 6.4,
        "nickname": "Jazz",
        "logo": "https://cdn.nba.com/logos/nba/1610612762/primary/L/logo.svg"
    },
    "Washington Wizards": {
        "arena": "Capital One Arena",
        "popularity": 6.5,
        "nickname": "Wizards",
        "logo": "https://cdn.nba.com/logos/nba/1610612764/primary/L/logo.svg"
    }
}

# Base prices for each seat type
BASE_PRICES = {
    "Upper Bowl": 50,
    "Lower Bowl": 200,
    "Courtside": 500
}

# ================== Price Calculation Model ==================
class NBAPricingModel:
    @staticmethod
    def calculate_price(home_team, away_team, seat_location, params):
        """Calculate dynamic ticket price based on multiple factors"""
        base = BASE_PRICES[seat_location]
        
        # Team popularity factor (average of both teams)
        popularity = (TEAM_DATA[home_team]['popularity'] + TEAM_DATA[away_team]['popularity']) / 20
        
        # Game importance factors
        rivalry = 1.3 if params['rivalry'] else 1.0
        national_tv = 1.2 if params['national_tv'] else 1.0
        
        # Team performance factors
        home_perf = 1 + (params['home_wins'] - 5) * 0.05
        away_perf = 1 + (params['away_wins'] - 5) * 0.03
        
        # Player factors
        star_power = 1 + params['spif'] / 50
        injury_effect = 0.8 if params['star_injured'] else 1.0
        
        # Calculate final price
        price = base * popularity * rivalry * national_tv * home_perf * away_perf * star_power * injury_effect * params['fec']
        
        # Apply seat location multiplier
        seat_multiplier = {
            "Upper Bowl": 1.0,
            "Lower Bowl": 1.8,
            "Courtside": 2.5
        }
        
        return max(50, min(3000, round(price * seat_multiplier[seat_location])))

# ================== Database Functions ==================
@st.cache_data
def get_historical_games(home_team_nickname):
    """Retrieve historical games from SQLite database"""
    db_path = os.getenv('NBA_DB_PATH', 'C:/Users/user/Projects/nba.sqlite')
    try:
        if not os.path.exists(db_path):
            st.error(f"Database file not found at {db_path}. Please download nba.sqlite from https://www.kaggle.com/datasets/wyattowalsh/basketball and place it in C:/Users/user/Projects.")
            return pd.DataFrame()
        if not os.access(db_path, os.R_OK):
            st.error(f"Permission denied: Cannot read {db_path}. Right-click the file > Properties > Security > Ensure your user has Read permissions.")
            return pd.DataFrame()
        
        conn = sqlite3.connect(db_path)
        # Verify table existence
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game'")
        if not cursor.fetchone():
            st.error(f"No 'game' table found in {db_path}. Please download the correct nba.sqlite from https://www.kaggle.com/datasets/wyattowalsh/basketball.")
            conn.close()
            return pd.DataFrame()
        
        query = """
        SELECT g.game_date, t1.nickname AS home, t2.nickname AS away, 
               g.pts_home AS home_team_score, g.pts_away AS visitor_team_score
        FROM game g
        JOIN team t1 ON g.team_id_home = t1.id
        JOIN team t2 ON g.team_id_away = t2.id 
        WHERE t1.nickname = ? AND strftime('%Y', g.game_date) = '2022'
        ORDER BY g.game_date DESC
        LIMIT 6
        """
        games = pd.read_sql(query, conn, params=(home_team_nickname,))
        conn.close()
        
        # Convert date format
        if not games.empty:
            games['game_date'] = pd.to_datetime(games['game_date']).dt.strftime('%b %d, %Y')
        
        return games
    
    except Exception as e:
        st.error(f"Database error: {str(e)}. Please ensure nba.sqlite is downloaded from https://www.kaggle.com/datasets/wyattowalsh/basketball and placed in {db_path} with correct permissions and schema (tables: game, team).")
        return pd.DataFrame()

@st.cache_data
def get_game_context(home_team, away_team):
    """Provide context based on historical games (not displayed in UI)"""
    db_path = os.getenv('NBA_DB_PATH', 'C:/Users/user/Projects/nba.sqlite')
    try:
        if not os.path.exists(db_path):
            return ""
        if not os.access(db_path, os.R_OK):
            return ""
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='game'")
        if not cursor.fetchone():
            conn.close()
            return ""
        
        query = """
        SELECT g.game_date, g.pts_home, g.pts_away
        FROM game g
        JOIN team t1 ON g.team_id_home = t1.id
        JOIN team t2 ON g.team_id_away = t2.id
        WHERE t1.nickname = ? AND t2.nickname = ? AND strftime('%Y', g.game_date) = '2022'
        ORDER BY g.game_date DESC
        LIMIT 5
        """
        games = pd.read_sql(query, conn, params=(TEAM_DATA[home_team]['nickname'], TEAM_DATA[away_team]['nickname']))
        conn.close()
        
        if not games.empty:
            wins = sum(1 for _, row in games.iterrows() if row['pts_home'] > row['pts_away'])
            ties = sum(1 for _, row in games.iterrows() if row['pts_home'] == row['pts_away'])
            total = len(games)
            win_rate = wins / total if total > 0 else 0
            if ties > 0:
                return f"{home_team} won {wins} and tied {ties} of their last {total} home games against {away_team} in 2022 ({win_rate:.0%} win rate)."
            return f"{home_team} won {wins} of their last {total} home games against {away_team} in 2022 ({win_rate:.0%} win rate)."
        return ""
    
    except Exception:
        return ""

# ================== UI Components ==================
def generate_price_report(home_team, away_team, price_details):
    """Generate CSV report of pricing details"""
    report = {
        "Home Team": home_team,
        "Away Team": away_team,
        "Arena": TEAM_DATA[home_team]['arena'],
        "Date": datetime.now().strftime("%Y-%m-%d"),
        **price_details
    }
    return pd.DataFrame([report])

def generate_price_comparison(home_team, away_team, params):
    """Generate a table comparing prices for all seat locations"""
    prices = []
    for seat in BASE_PRICES.keys():
        price = NBAPricingModel.calculate_price(home_team, away_team, seat, params)
        prices.append({"Seat Location": seat, "Price": f"${price:,.0f}"})
    return pd.DataFrame(prices)

# ================== Streamlit App ==================
def main():
    # Configure page
    st.set_page_config(
        layout="wide",
        page_title="NBA Dynamic Pricing Pro",
        page_icon="🏀"
    )
    
    # Custom CSS with improved text visibility
    st.markdown("""
    <style>
    .main { 
        background: url('https://www.nba.com/assets/images/backgrounds/basketball-court.jpg') no-repeat center center fixed;
        background-size: cover;
        color: #1D428A;
    }
    .header { 
        color: #000000; 
        text-shadow: 2px 2px 3px rgba(255,255,255,0.8);
        font-family: 'Arial Black', sans-serif;
    }
    .team-card {
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s, box-shadow 0.2s;
        color: #1D428A;
    }
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    .price-badge {
        background: linear-gradient(45deg, #1D428A, #C8102E);
        color: #FFFFFF;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-size: 1.2rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background: #1D428A;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        transition: background 0.2s;
    }
    .stButton>button:hover {
        background: #C8102E;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        color: #1D428A;
    }
    .stSelectbox, .stSlider, .stCheckbox {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        padding: 10px;
        color: #1D428A;
    }
    .stDataFrame {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 10px;
        padding: 10px;
        color: #1D428A;
    }
    .stMarkdown, .stText, .stInfo, .stWarning {
        background: rgba(255, 255, 255, 0.95);
        padding: 10px;
        border-radius: 8px;
        color: #1D428A;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.title("🏀 NBA Dynamic Pricing Engine")
    st.markdown("---")
    
    # Main layout
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown('<h2 class="header">Configure Your Game</h2>', unsafe_allow_html=True)
        
        # Team selection with logos
        team_names = list(TEAM_DATA.keys())
        col_team1, col_team2 = st.columns(2)
        with col_team1:
            home_team = st.selectbox("Home Team", team_names, index=team_names.index("Los Angeles Lakers"), help="Select the home team")
            try:
                st.image(TEAM_DATA[home_team]['logo'], width=100, caption="Home Team")
            except:
                st.warning("Home team logo unavailable")
        with col_team2:
            away_team = st.selectbox("Away Team", [t for t in team_names if t != home_team], help="Select the away team")
            try:
                st.image(TEAM_DATA[away_team]['logo'], width=100, caption="Away Team")
            except:
                st.warning("Away team logo unavailable")
        
        # Pricing parameters
        st.subheader("Pricing Factors")
        with st.expander("Adjust Pricing Parameters", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                seat_location = st.selectbox("Seat Location", list(BASE_PRICES.keys()), help="Choose your seating area")
                home_wins = st.slider("Home Team Wins (Last 10)", 0, 10, 6, help="Wins in last 10 games")
                away_wins = st.slider("Away Team Wins (Last 10)", 0, 10, 4, help="Wins in last 10 games")
                spif = st.slider("Star Power Index (SPIF)", 0, 50, 35, help="Star player impact (0-50)")
            with col_b:
                fec = st.slider("Fan Engagement (FEC)", 0.5, 1.5, 1.1, step=0.1, help="Fan engagement level")
                rivalry = st.checkbox("Rivalry Game", value=True, help="Is this a rivalry game?")
                national_tv = st.checkbox("National TV Game", value=True, help="Is the game on national TV?")
                star_injured = st.checkbox("Star Player Injured", help="Is the star player injured?")
        
        # Calculate price
        params = {
            'home_wins': home_wins,
            'away_wins': away_wins,
            'spif': spif,
            'fec': fec,
            'rivalry': rivalry,
            'national_tv': national_tv,
            'star_injured': star_injured
        }
        
        price = NBAPricingModel.calculate_price(home_team, away_team, seat_location, params)
        
        # Display price
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <h3>Recommended Ticket Price</h3>
            <div class="price-badge">${price:,.0f}</div>
            <p>{seat_location} Seating • {TEAM_DATA[home_team]['arena']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Price comparison table
        st.subheader("Price Comparison")
        price_df = generate_price_comparison(home_team, away_team, params)
        st.dataframe(price_df, use_container_width=True)
        
        # Price breakdown
        with st.expander("Price Breakdown"):
            st.write(f"**Base Price:** ${BASE_PRICES[seat_location]:,.0f}")
            st.write(f"**Team Popularity:** +{((TEAM_DATA[home_team]['popularity'] + TEAM_DATA[away_team]['popularity']) / 20 - 1):.0%}")
            st.write(f"**Rivalry Game:** {'+30%' if rivalry else 'No effect'}")
            st.write(f"**National TV:** {'+20%' if national_tv else 'No effect'}")
            st.write(f"**Star Power:** +{spif/50:.0%}")
            st.write(f"**Fan Engagement:** {fec:.1f}x")
            st.write(f"**Home Performance:** {1 + (params['home_wins'] - 5) * 0.05:.2f}x")
            st.write(f"**Away Performance:** {1 + (params['away_wins'] - 5) * 0.03:.2f}x")
            st.write(f"**Injury Effect:** {'-20%' if star_injured else 'No effect'}")
    
    with col2:
        st.markdown('<h2 class="header">Historical Examples</h2>', unsafe_allow_html=True)
        
        # Historical games
        games = get_historical_games(TEAM_DATA[home_team]['nickname'])
        
        if not games.empty:
            for _, game in games.iterrows():
                with st.container():
                    # Calculate hypothetical price
                    hist_params = {
                        'home_wins': np.random.randint(4, 8),
                        'away_wins': np.random.randint(3, 7),
                        'spif': np.random.randint(20, 45),
                        'fec': round(np.random.uniform(0.8, 1.3), 1),
                        'rivalry': np.random.choice([True, False], p=[0.3, 0.7]),
                        'national_tv': np.random.choice([True, False]),
                        'star_injured': False
                    }
                    
                    hist_price = NBAPricingModel.calculate_price(
                        home_team,
                        next(k for k,v in TEAM_DATA.items() if v['nickname'] == game['away']),
                        "Upper Bowl",
                        hist_params
                    )
                    
                    # Display game card
                    st.markdown(f"""
                    <div class="team-card">
                        <h4>{game['game_date']}</h4>
                        <p>{home_team} vs {game['away']}</p>
                        <p>Score: {game['home_team_score']}-{game['visitor_team_score']}</p>
                        <div class="price-badge">${hist_price:,.0f}</div>
                        <small>Upper Bowl estimate</small>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No historical games found in database")
            st.info("Please ensure nba.sqlite is in C:/Users/user/Projects with correct permissions and schema (tables: game, team)")
        
        # Download report
        st.markdown("---")
        st.subheader("Export Pricing")
        report = generate_price_report(home_team, away_team, {
            "Seat Location": seat_location,
            "Final Price": price,
            **params
        })
        st.download_button(
            label="Download Price Report",
            data=report.to_csv(index=False),
            file_name=f"nba_pricing_{home_team}_{away_team}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #1D428A; padding: 1rem;">
        NBA Dynamic Pricing System © 2025 | Powered by ELEC3544
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()