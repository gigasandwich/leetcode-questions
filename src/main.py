from src.question import Question
from typing import List
from requests import request
from fpdf import FPDF

def main():
    filepath = 'questions_links.txt'

    print(f'Getting all the questions from file "{filepath}"')
    links: list = get_questions_links(filepath)

    print('Fetching and parsing questions from the website')
    questions: list = parse_to_questions(links)

    print('Merging and formating all the questions')
    questions_str: str = questions_to_str(questions)

    export_to_txt(questions_str)
    export_to_pdf(questions)

##############################
# pdf export
##############################
def export_to_pdf(questions: List[Question]) -> None:
    pdf= FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_page()
    pdf.set_font('Arial', size=16, style='BI')
    pdf.cell(0, 10, txt='LeetCode questions (Sandwich edition xD)', ln=True, align='C') # Header
    pdf.ln(10)

    for index, question in enumerate(questions):
        if index > 0:
            pdf.add_page() # New page for each question except the first one

        # Title
        pdf.set_font('Arial', size=14, style='B')
        pdf.cell(0, 7,'----------------------------------------' , ln=True, align='C')
        pdf.cell(0, 8, question.title, ln=True, align='C')
        pdf.ln(10)

        # Body
        pdf.set_font('Arial', size=11)
        pdf.multi_cell(0, 6, question.body)

    pdf.output('output/leetcode-questions.pdf')

##############################
# txt export
##############################
def export_to_txt(questions: str) -> None:
    with open ('output/leetcode-questions.txt', 'w') as file:
        file.write(questions)
    print("Exported to txt!")

def questions_to_str(questions: list) -> str :
    def question_to_str(question: Question):
        text = ''
        text += f'{question.title}\n\n\n'
        text += f'{question.body}\n'
        text += f'\n-------------------------\n'
        return text
    
    text = ''
    for question in questions:
        text += question_to_str(question)

    return text

##############################
# Other main methods
##############################
def parse_to_questions(links: list) -> List[Question] :
    '''
    Fetches the questions from the urls as html string and then parses it to Question object
    '''
    ##############################
    # Dummy test
    ##############################
    with open('dummy/two-sums.html', 'r') as html:
        question = Question(html.read())
    questions = []
    questions.append(question)
    return questions
    ##############################
    # Dummy test
    ##############################

    def fetch_question(link: str):
        response = request.__get__(link)
        return f'{link}'
    
    questions_html = list(fetch_question(link) for link in links)
    questions = list(Question(question_html) for question_html in questions_html)

    return questions

def get_questions_links(filepath: str) -> list : 
    '''
    Gets the urls of the leetcode questions from a file from a file
    '''
    links = ()

    try:
        with open(filepath) as f:
           links = list(link.strip() for link in tuple(f.readlines()) if '/problems/' in link) # Using tuple to make sure there's no double
    except FileNotFoundError as e:
        print(e)
        
    return links # eg: ('https://leetcode.com/problems/two-sum')

if __name__ == '__main__':
    main()