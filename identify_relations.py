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
    for msg in data[:1000]:
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
        f"You're an email classification system.\n"
        f"Here's the sender : {author}\n"
        f"Here are the contents of the email :\n\"{content}\"\n\n"
        "Does this message come from a person speaking directly to a human? "
        "(such as a business or personal contact), or is it an automatic message "
        "(newsletter, advertising, service notification)?\n\n"
        "Just answer 'true' if it's a human, or 'false' if it's automatic."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        reply = response.choices[0].message.content.strip().lower()
        return reply.startswith("true")
    except Exception as e:
        print(f"API error: {e}")
        return None


if __name__ == "__main__":
    relations = identify_relations("emails.json")
    with open("relations.json", "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)

    print("The relations have been saved in ‘relations.json’.")