import os
import tweepy
import requests
import google.generativeai as genai
from mistralai import Mistral
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("No GOOGLE_API_KEY found in environment variables. Please create a .env file and add it.")

serper_api=os.getenv("SERPER_API_KEY")
if not serper_api:
    raise ValueError("No SERPER_API_KEY found in environment variables. Please create a .env file and add it.")

mistral_api = os.getenv("MISTRAL_API_KEY")
if not mistral_api:
    raise ValueError("No MISTRAL_API_KEY found in environment variables. Please create a .env file and add it.")

client = tweepy.Client(bearer_token=os.getenv("BEARER_TOKEN"))
if not client:
    raise ValueError("No BEARER_TOKEN found in environment variables. Please create a .env file and add it.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

mistral_client = Mistral(api_key=mistral_api)

def get_news(query):
    """
    Cherche les dernières actualités sur le web (Serper), Twitter et MyAnimeList (Jikan),
    puis demande à Gemini de synthétiser et expliquer ces actualités à l'utilisateur.
    """
    try:
        # Recherche web avec Serper
        web_results = search_serper(query)
        web_text = "\n".join(web_results)

        # Recherche Twitter
        # twitter_results = search_twitter(query)
        # twitter_text = "\n".join(twitter_results)

        # Recherche Jikan
        # jikan_results = search_jikan(query)
        # jikan_text = "\n".join(jikan_results)

        # Préparer le prompt pour Gemini
        prompt = (
            f"Voici des résultats web sur '{query}':\n{web_text}\n\n"
            # f"Voici des tweets récents:\n{twitter_text}\n\n"
            # f"Voici des actualités MyAnimeList:\n{jikan_text}\n\n"
            f"En tant qu'expert anime/manga, synthétise et explique les dernières actualités pour l'utilisateur de façon claire, concise et pédagogique."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"


def search_twitter(query, max_results=10):
    prompt = f"""Tu es un expert en twitter API query.
    Tu dois écrire une requête pour rechercher les tweets récents sur le sujet donné.
    - Exemple de requête : "anime OR manga -is:retweet lang:en"
    - Tu dois retourner uniquement la requête, sans explications.
    Sujet : {query}
    """
    response = mistral_client.chat.complete(
        model="mistral-medium-2505",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    query_formated = response.choices[0].message.content.strip()

    tweets = client.search_recent_tweets(query=query_formated, tweet_fields=['context_annotations', 'created_at'], max_results=max_results)
    return [tweet.text for tweet in tweets.data] if tweets.data else ["Aucun tweet trouvé."]


def search_jikan(query):
    pass
#     url = f"https://api.jikan.moe/v4/anime?q={query}&order_by=start_date&sort=desc"
#     resp = requests.get(url)
#     if resp.ok:
#         data = resp.json()
#         results = []
#         for anime in data.get("data", [])[:5]:
#             results.append(f"{anime['title']} ({anime['year']}): {anime['synopsis'][:100]}...")
#         return results
#     return ["Aucune actualité trouvée sur MyAnimeList."]

def search_serper(query, max_results=5):
    """
    Search the web using Serper API
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "hl": "fr",
        "num": 5
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data.get("organic", [])[:max_results]:
            results.append(f"{item['title']}: {item['link']}")
        return results
    return ["Aucune actualité trouvée."]