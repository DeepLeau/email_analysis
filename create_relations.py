import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)

def extract_interest_centers(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    relations_interest_centers = {}
    for author, content in data.items():
        prompt = f"From the content of all emails : {content}, could you tell me the expertise/interest zone of the user ? Only return the interest centers/expertise in words separated by a coma"
        res = generate_response_by_ai(prompt)
        relations_interest_centers[author] = res
    return relations_interest_centers

def get_number_of_interactions(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    number_interactions = {}
    for author, content in data.items():
        number_interactions[author] = len(content)
    return number_interactions

def get_relationships_proximity(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    relationship_proximity = {}
    for author, content in data.items():
        prompt = f"Indicate how close I am to the people who sent me this type of e-mail: {content}. You can indicate family, professional background, community or anything else you deem appropriate. One-word answers"
        proximity = generate_response_by_ai(prompt)
        relationship_proximity[author] = proximity
    return relationship_proximity

def get_trust(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    relations_trust = {}
    for author, content in data.items():
        prompt = f"Indicate the level of trust I have to the people who sent me this type of e-mail: {content}. Choose between : very high, high, medium, low, very low. One-word answers"
        trust = generate_response_by_ai(prompt)
        relations_trust[author] = trust
    return relations_trust


def generate_response_by_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        reply = response.choices[0].message.content.strip().lower()
        return reply
    except Exception as e:
        print(f"API error: {e}")
        return None


if __name__=="__main__":
    json_file = "relations.json"

    # Extract interest centers
    interest_centers = extract_interest_centers(json_file)
    print(interest_centers)

    # Get interactions frequency
    interactions = get_number_of_interactions(json_file)
    print(interactions)

    # Get trust level
    trust = get_trust(json_file)
    print(trust)

    # Get relationships proximity
    proximity = get_relationships_proximity(json_file)
    print(proximity)


