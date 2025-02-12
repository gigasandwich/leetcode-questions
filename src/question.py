from bs4 import BeautifulSoup

class Question:
    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Title eg: "{Problem name} - LeetCode"
        title = soup.find('title').string.split('-')[0]
        # Body eg: <meta name="description" content=" Two Sum - Given an array of integers nums ...>
        meta_description = soup.find('meta', attrs= {'name' : 'description'})

        self.title = title
        self.body = meta_description['content']
    
    def __str__(self):
        text = ''
        text += f'{self.title}\n\n\n'
        text += f'{self.body}\n'
        text += f'\n-------------------------\n'
        return text
    
    def to_string(self):
        return self.__str__