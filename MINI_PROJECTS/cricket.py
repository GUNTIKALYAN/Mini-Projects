import streamlit as st
import google.generativeai as genai
import json
import os

# ✅ Use Your Google Gemini API Key
# API_KEY = "PI KEY"
# genai.configure(api_key=API_KEY)

# ✅ Function to Fetch Cricket Player Stats
def get_cricket_player_stats(player_name):
    """Fetch cricket player stats using Google Gemini API."""

    # ✅ Define the AI prompt
    prompt = f"""
    Provide detailed career statistics of the cricket player '{player_name}' in JSON format, including:
    - Full Name
    - Date of Birth (YYYY-MM-DD)
    - Nationality
    - Playing Role (Batsman, Bowler, All-rounder, Wicketkeeper)
    - Batting Style (Right-hand, Left-hand)
    - Bowling Style (Fast, Spin, Medium)
    - Total Matches
    - Total Runs
    - Batting Average
    - Strike Rate
    - Total Wickets
    - Bowling Average
    - Best Bowling Figures

    Response format:
    ```
    {{
        "player": {{
            "full_name": "Virat Kohli",
            "date_of_birth": "1988-11-05",
            "nationality": "India",
            "playing_role": "Batsman",
            "batting_style": "Right-hand",
            "bowling_style": "Medium",
            "total_matches": 500,
            "total_runs": 25000,
            "batting_average": 55.3,
            "strike_rate": 89.5,
            "total_wickets": 10,
            "bowling_average": 45.2,
            "best_bowling_figures": "3/12"
        }}
    }}
    ```
    """

    try:
        # ✅ Use Gemini API to generate content
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)

        if response and response.text:
            # ✅ Extract JSON from AI response
            start = response.text.find("{")
            end = response.text.rfind("}") + 1
            json_string = response.text[start:end]

            # ✅ Validate and parse JSON
            try:
                player_data = json.loads(json_string)
                return player_data
            except json.JSONDecodeError:
                st.error("❌ AI response is not valid JSON.")
                st.write("🔍 **Raw AI Response:**", response.text)  # Debugging output
                return None
        else:
            st.error("❌ Unexpected API response format.")
            return None

    except Exception as e:
        st.error(f"❌ Exception occurred: {e}")
        return None


# ✅ Apply Custom Styling using CSS
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
        }
        .stTextInput>div>div>input {
            font-size: 18px !important;
            padding: 10px;
            border-radius: 8px;
        }
        .stButton>button {
            font-size: 18px !important;
            border-radius: 8px;
            padding: 8px 16px;
            background-color: #007BFF;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        .player-card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .player-title {
            font-size: 24px;
            font-weight: bold;
            color: #28a745;
        }
        .player-info {
            font-size: 16px;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)


# ✅ Streamlit App UI
st.title("🏏 Cricket Player Stats Finder")
st.write("Enter a **Cricket Player's Name** to fetch their **career statistics** including **runs, wickets, and averages.**")

# **User Input**
player_name = st.text_input("Enter Cricketer's Name")

if st.button("🔍 Get Stats"):
    if not player_name.strip():
        st.warning("⚠️ Please enter a cricketer's name.")  # ✅ Warns if no name is entered
    else:
        player_data = get_cricket_player_stats(player_name)

        if player_data:
            player = player_data.get("player", {})

            st.subheader(f"🏏 Stats for **{player.get('full_name', player_name)}**")

            # ✅ Display player stats in a stylish format
            st.markdown(f"""
            <div class="player-card">
                <p class="player-title">{player.get("full_name", "Unknown")}</p>
                <p class="player-info"><b>Date of Birth:</b> {player.get("date_of_birth", "N/A")}</p>
                <p class="player-info"><b>Nationality:</b> {player.get("nationality", "N/A")}</p>
                <p class="player-info"><b>Playing Role:</b> {player.get("playing_role", "N/A")}</p>
                <p class="player-info"><b>Batting Style:</b> {player.get("batting_style", "N/A")}</p>
                <p class="player-info"><b>Bowling Style:</b> {player.get("bowling_style", "N/A")}</p>
                <p class="player-info"><b>Total Matches:</b> {player.get("total_matches", "N/A")}</p>
                <p class="player-info"><b>Total Runs:</b> {player.get("total_runs", "N/A")}</p>
                <p class="player-info"><b>Batting Average:</b> {player.get("batting_average", "N/A")}</p>
                <p class="player-info"><b>Strike Rate:</b> {player.get("strike_rate", "N/A")}</p>
                <p class="player-info"><b>Total Wickets:</b> {player.get("total_wickets", "N/A")}</p>
                <p class="player-info"><b>Bowling Average:</b> {player.get("bowling_average", "N/A")}</p>
                <p class="player-info"><b>Best Bowling Figures:</b> {player.get("best_bowling_figures", "N/A")}</p>
            </div>
            """, unsafe_allow_html=True)

            # ✅ Save to JSON file
            file_path = os.path.join(os.getcwd(), "cricket_player_stats.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(player_data, f, indent=4, ensure_ascii=False)

            st.success(f"✅ Data saved to `{file_path}`")
