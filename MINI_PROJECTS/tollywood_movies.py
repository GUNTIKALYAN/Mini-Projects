
import streamlit as st
import google.generativeai as genai
import json
import os

# ✅ Set Your Google Gemini API Key
# API_KEY = "API KEY"
# genai.configure(api_key=API_KEY)

# ✅ Function to Fetch Movies by Actor
def get_movies_by_actor(actor_name):
    """Fetch Tollywood movies featuring the given actor using Google Gemini API."""

    # ✅ Define the AI prompt
    prompt = f"""
    List 10 popular Tollywood movies starring '{actor_name}' with details in JSON format:
    - Movie Name
    - Release Date (YYYY-MM-DD)
    - Director
    - Genre
    - Budget in Crores
    - Estimated Profit in Crores

    Response format:
    ```
    {{
        "movies": [
            {{
                "movie_name": "Example Movie",
                "release_date": "2024-05-10",
                "director": "Director Name",
                "genre": "Action",
                "budget_crores": 50,
                "estimated_profit_crores": 120
            }},
            ...
        ]
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
                movie_data = json.loads(json_string)
                return movie_data
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
        .movie-card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }
        .movie-title {
            font-size: 22px;
            font-weight: bold;
            color: #ff5733;
        }
        .movie-info {
            font-size: 16px;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)


# ✅ Streamlit App UI
st.title("🎬 Tollywood Movie Finder")
st.write("Enter a Tollywood actor's name to get their **popular movies** with **release dates, budgets, and profits.**")

# User Input
actor_name = st.text_input("Enter Actor's Name")

if st.button("🔍 Get Movies"):
    if actor_name:
        movies_data = get_movies_by_actor(actor_name)

        if movies_data:
            st.subheader(f"🎥 Movies featuring **{actor_name}**")

            # ✅ Display movies in a stylish format
            for movie in movies_data.get("movies", []):
                st.markdown(f"""
                <div class="movie-card">
                    <p class="movie-title">{movie["movie_name"]}</p>
                    <p class="movie-info"><b>Release Date:</b> {movie["release_date"]}</p>
                    <p class="movie-info"><b>Director:</b> {movie["director"]}</p>
                    <p class="movie-info"><b>Genre:</b> {movie["genre"]}</p>
                    <p class="movie-info"><b>Budget:</b> ₹{movie["budget_crores"]} crores</p>
                    <p class="movie-info"><b>Estimated Profit:</b> ₹{movie["estimated_profit_crores"]} crores</p>
                </div>
                """, unsafe_allow_html=True)

            # ✅ Save to JSON file
            file_path = os.path.join(os.getcwd(), "tollywood_movies.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(movies_data, f, indent=4, ensure_ascii=False)

            st.success(f"✅ Data saved to `{file_path}`")
    else:
        st.warning("⚠️ Please enter an actor's name.")
