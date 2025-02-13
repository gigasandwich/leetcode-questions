from src.question import *
from src.pdf import *
from typing import List

def main():
    filepath = 'questions_links.txt'

    try:
        print(f'Getting all the questions from file "{filepath}"...')
        links: List[str] = get_questions_links(filepath)

        print('Fetching and parsing questions from the website...')
        questions: List[Question] = parse_to_questions(links)

        print('Merging and formating all the questions...')
        export_to_txt(questions)
        export_to_pdf(questions)
        print('Export successful!')
    except Exception as e:
        print(f'\nERROR: {e}\n')

##############################
# Exports
##############################

def export_to_pdf(questions: List[Question]) -> None:
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    for index, question in enumerate(questions):
        if index > 0:
            pdf.add_page()  # New page for each question except the first one
        
        pdf.chapter_title(question.title)
        pdf.chapter_body(question.body.strip())

    pdf.output("output/leetcode-questions.pdf", "F")

def export_to_txt(questions: list) -> None:
    text = ''
    for question in questions:
        text += question.__str__()

    with open ('output/leetcode-questions.txt', 'w') as file:
        file.write(text)

##############################
# Data fetching
##############################

def parse_to_questions(links: list) -> List[Question] :
    '''
    Fetches the questions from the urls as html string and then parses it to Question object
    Now it uses GraphQL API of LeetCode
    '''
    questions_json = list(fetch_question(link) for link in links)
    questions = list(Question(question_json) for question_json in questions_json)
    return questions

def get_questions_links(filepath: str) -> list : 
    '''
    Gets the urls of the leetcode questions from a file
    '''
    links = []

    try:
        with open(filepath) as f:
           links = list(link.strip() for link in tuple(f.readlines()) if '/problems/' in link) # Using tuple to make sure there's no double
    except FileNotFoundError as e:
        raise e
        
    return links # eg: ('https://leetcode.com/problems/two-sum')

if __name__ == '__main__':
    main()