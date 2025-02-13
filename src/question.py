import requests
from bs4 import BeautifulSoup

class Question:
    def __init__(self, json_response: dict):
        """
        Constructor based on JSON data from LeetCode's GraphQL API.
        """
        title = json_response['title']
        body = ''
        content = json_response['content']

        soup = BeautifulSoup(content, 'html.parser')
        body = soup.get_text()

        self.title = title
        self.body = body
    
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
            question: dict = data["data"]["question"] # contains "title" and "content" as its keys
            return question
        else:
            raise Exception(f"Failed to fetch problem: {slug} (Status: {response.status_code})")