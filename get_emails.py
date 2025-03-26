from apiclient import discovery, errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
from time import strftime, gmtime
import sys
import json

def ReadEmailDetails(service, user_id, msg_id):
    temp_dict = {}
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = message.get('payload', {})
        headers = payload.get('headers', [])

        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')
            if name == 'subject':
                temp_dict['Subject'] = value
            elif name == 'date':
                temp_dict['DateTime'] = value
            elif name == 'from':
                temp_dict['From'] = value

        def get_body(payload):
            if 'parts' in payload:
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data')
                        if data:
                            decoded = base64.urlsafe_b64decode(data).decode('utf-8')
                            return decoded
                    elif part['mimeType'] == 'text/html':
                        data = part['body'].get('data')
                        if data:
                            decoded = base64.urlsafe_b64decode(data).decode('utf-8')
                            soup = BeautifulSoup(decoded, 'lxml')
                            return soup.get_text()
            else:
                body = payload.get('body', {}).get('data')
                if body:
                    decoded = base64.urlsafe_b64decode(body).decode('utf-8')
                    return decoded
            return ''

        temp_dict['Message_body'] = get_body(payload)

    except Exception as e:
        print(f"Erreur sur le mail {msg_id} :", e)
        temp_dict = None

    return temp_dict

def ListAllMessages(service, user_id):
    try:
        response = service.users().messages().list(userId=user_id, maxResults=500).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id,
                pageToken=page_token,
                maxResults=500
            ).execute()
            messages.extend(response['messages'])
            print(f"... {len(response['messages'])} emails de plus récupérés, {len(messages)} au total")
            sys.stdout.flush()

        return messages

    except errors.HttpError as error:
        print(f'Erreur HTTP : {error}')
        return []

if __name__ == "__main__":
    print('\n--- Démarrage de la récupération des emails ---')

    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)

    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))
    user_id = 'me'

    print('\n--- Récupération de la liste des messages ---')
    email_list = ListAllMessages(GMAIL, user_id)

    rows = 0
    filename = f'emails_{strftime("%Y_%m_%d_%H%M%S", gmtime())}.json'
    all_emails = []

    print('\n--- Récupération du contenu des emails ---')

    for email in email_list:
        msg_id = email['id']
        email_data = ReadEmailDetails(GMAIL, user_id, msg_id)
        if email_data:
            all_emails.append(email_data)
            rows += 1

        if rows > 0 and rows % 50 == 0:
            print(f"... {rows} emails traités")
            sys.stdout.flush()

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_emails, f, ensure_ascii=False, indent=2)

    print(f'\n✅ {rows} emails exportés dans "{filename}"')
    print('--- Terminé ---')
