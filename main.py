def main():
    links = get_question_links('question_links.txt')
    questions = fetch_questions(links)
    questions_str = merge_and_format_questions(questions)
    export_to_txt(questions_str)

##############################
# Helper methods
##############################
def export_to_txt(questions: str) -> None:
    print("Exported!")

def merge_and_format_questions(questions: list) -> str :
    print('Merging and formating all the questions')
    text = 'Question1' + '------' + 'Question2'

def fetch_questions(links: list) -> list :
    print('Fetching questions from the website')
    return ('Question1', 'Question2')

def get_question_links(filepath: str) -> list : 
    print(f'Getting all the questions from file "{filepath}"')
    return ('https://leetcode.com/problems/fako', 'https://leetcode.com/problems/dummy')

if __name__ == '__main__':
    print()
    main()
    print()