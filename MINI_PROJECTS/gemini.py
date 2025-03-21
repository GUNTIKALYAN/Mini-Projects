import requests
import json
url = "https://gemini-pro-ai.p.rapidapi.com/"

payload = { "contents": [
		{
			"role": "user",
			"parts": [{ "text": "Hello" }]
		}
	] }
headers = {
	# "x-rapidapi-key": "API KEY",
	"x-rapidapi-host": "gemini-pro-ai.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

if response.status_code == 200:  # Check if the request was successful
    data = response.json()
    with open("C:/Users/Kalyan/OneDrive/Desktop/fetching_data/gemini_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False) #added ensure_ascii=false to support all languages.
    print("Data downloaded and saved to gemini_data.json")
else:
    print(f"Error: Failed to fetch data. Status code: {response.status_code}")
    print(response.text) #print the response text to help debugging.