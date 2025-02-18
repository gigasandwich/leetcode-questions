import requests
from bs4 import BeautifulSoup

class Question:
    def __init__(self, json_response: dict):
        """
        Constructor based on JSON data from LeetCode's GraphQL API.
        """
        title = json_response['title']
        body = ''
        code_blocks = []

        content = json_response['content']
        soup = BeautifulSoup(content, 'html.parser')

        # Error handling
        if content is None:
            print(f"No content found for '{self.title}'. It might be a locked problem.")
            self.body = "Content is unavailable."
            self.code_blocks = []
            return

        for element in soup.contents:
            if element.name == "pre":
                body += f"\n```\n{element.get_text().strip()}\n```\n\n"
            elif element.name == "p":
                body += f"{element.get_text().strip()}\n\n"
            elif element.name == "ul":
                for li in element.find_all("li"):
                    body += f"- {li.get_text().strip()}\n"
            elif element.name == "strong" or element.name == "em":
                body += f"{element.get_text().strip()}\n"
            elif element.name == "code":
                body += f"``{element.get_text().strip()}``\n"
            else:
                body += element.get_text() + "\n"

        self.title = title
        self.body = body
        self.code_blocks = code_blocks 
    
    def __str__(self):
        text = ''
        text += f'{self.title}\n\n\n'
        text += f'{self.body}\n'
        text += f'\n-------------------------\n'
        return text
    
    def to_string(self):
        return self.__str__()

##############################
# Static question Methods
##############################

def extract_slug(link: str) -> str:
    '''
    The pattern of a link looks like this: 
    https://leetcode.com/problems/{slug}
    '''
    return link.rstrip('/').split("/")[-1]

def fetch_question(link: str) -> dict:
    slug = extract_slug(link)
    url = 'https://leetcode.com/graphql'
    headers = {
        'Content-Type': 'application/json',
        'Referer': f'https://leetcode.com/problems/{slug}',
        'User-Agent': 'Mozilla/5.0'
    }
    query = {
        'query': '''
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                title
                content
                difficulty
            }
        }
        ''',
        'variables': {'titleSlug': slug}
    }

    response = requests.post(url, json=query, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Check if data structure is correct
        if 'data' in data and data['data'] and 'question' in data['data']:
            return data['data']['question']
        else:
            print(f"Missing 'question' or 'data' for '{slug}'")
            return None
    else:
        raise Exception(f"Failed to fetch problem: {slug} (Status: {response.status_code})")