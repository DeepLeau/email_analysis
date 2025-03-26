import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)


def identify_relations(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    relations = {}
    blacklist = []
    for msg in data:
        content = msg['Message_body']
        author = msg['From']
        if author not in blacklist:
            res = ai_identify(content, author)
            if res == True:
                if author in relations.keys():
                    relations[author].append(content)
                else:
                    relations[author] = [content]
            else:
                blacklist.append(author)
    return relations


def ai_identify(content, author, max_chars=100):
    content = content[:max_chars]

    prompt = (
        f"Tu es un système de classification d'emails.\n"
        f"Voici l'expéditeur : {author}\n"
        f"Voici le contenu de l'email :\n\"{content}\"\n\n"
        "Est-ce que ce message vient d'une personne qui s'adresse à un humain directement "
        "(comme un contact professionnel ou personnel), ou bien est-ce un message automatique "
        "(newsletter, publicité, notification de service) ?\n\n"
        "Réponds uniquement par 'oui' si c'est un humain, ou 'non' si c'est automatique."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        reply = response.choices[0].message.content.strip().lower()
        return reply.startswith("oui")
    except Exception as e:
        print(f"Erreur API: {e}")
        return None


if __name__ == "__main__":
    relations = identify_relations("emails.json")
    with open("relations.json", "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)

    print("✅ Les relations ont été enregistrées dans 'relations.json'")