def main():
    filepath = 'questions_links.txt'

    print(f'Getting all the questions from file "{filepath}"')
    links: list = get_questions_links(filepath)
    print(links)

    print('Fetching questions from the website')
    questions: list = fetch_questions(links)

    print('Merging and formating all the questions')
    questions_str: str = merge_and_format_questions(questions)

    export_to_txt(questions_str)

##############################
# Helper methods
##############################

def export_to_txt(questions: str) -> None:
    with open ('output/leetcode-questions.txt', 'w') as file:
        file.write(questions)
    print("Exported!")

def merge_and_format_questions(questions: tuple) -> str :
    text = ''
    for question in questions:
        # Title
        text += f'{question}\n'
        # text += f'{question.title}'
        # text += f'{question.body}'
        
        # Next question
        text += f'\n-------------------------\n'
    return text

def fetch_questions(links: tuple) -> tuple :
    def fetch_question(link: str):
        return f'{link}'

    questions = tuple((fetch_question(link) for link in links))
    return questions

def get_questions_links(filepath: str) -> tuple : 
    links = ()

    try:
        with open(filepath) as file:
           links = tuple((link.strip() for link in file.readlines() if '/problems/' in link))
    except FileNotFoundError as e:
        print(e)
        
    return links # eg: ('https://leetcode.com/problems/two-sum')

if __name__ == '__main__':
    print()
    main()
    print()