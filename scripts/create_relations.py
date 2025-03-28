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
        prompt = f"From the content of all emails : {content}, could you tell me the expertise/interest zone of the user ? Only return the interest centers/expertise in words separated by a coma. Don't return too many interest centers/expertise, focus on general ones."
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
    

def build_combined_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    interest_centers = extract_interest_centers(json_file)
    interactions = get_number_of_interactions(json_file)
    trust_levels = get_trust(json_file)
    proximity_levels = get_relationships_proximity(json_file)

    final_data = []

    for sender in data.keys():
        email_info = {
            "sender": sender,
            "trust": trust_levels.get(sender, "unknown").capitalize() + " trust",
            "interactions_frequency": interactions.get(sender, 0),
            "relationship_context": proximity_levels.get(sender, "Unknown").capitalize(),
            "expertise": [e.strip().capitalize() for e in interest_centers.get(sender, "").split(",") if e],
            "relationship_duration": "Unknown",  
            "exchange_balance": 1.0,  
            "relations_connections": []  
        }
        final_data.append(email_info)

    with open("./data/relations_modelization.json", "w", encoding='utf-8') as f_out:
        json.dump(final_data, f_out, indent=2)


if __name__=="__main__":
    json_file = "./data/relations.json"

    build_combined_json(json_file)


