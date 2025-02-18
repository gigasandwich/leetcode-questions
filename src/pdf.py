import re
from src.question import *
from typing import List
from fpdf import FPDF

class PDF (FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.first_page = True
        self.add_font('DejaVu', '', 'assets/fonts/DejaVuSans.ttf', uni=True)

    def header(self):
        if self.first_page:
            self.set_font('Arial', 'BI', 16)
            self.cell(0, 10, 'LeetCode Questions (Sandwiched)', ln=True, align='C')
            self.ln(10)
            self.first_page = False
        
    def chapter_title(self, title):
        '''
        Sets the centered title
        '''
        self.set_font('DejaVu', '', 14)
        self.cell(0, 8, title, ln=True, align='C')
        self.ln(5)
    
    def chapter_body(self, body):
        '''
        Sets the main content of each question
        '''
        self.set_font("DejaVu", "", 12)
    
        body = re.sub(r'<pre><code>(.*?)</code></pre>', r'```\1```', body, flags=re.DOTALL) # <pre><code> => ``` for code blocks
        body = re.sub(r'<code>(.*?)</code>', r'`\1`', body)  # Inline code
        
        lines = body.split("\n")

        in_code_block = False
        code_block_lines = []

        for line in lines:
            line = line.strip()

            # Detecting the start/end of a code block (```)
            if line.startswith("```"):
                
                if in_code_block:
                    # End of code block
                    self.set_font("Courier", "", 11)
                    self.set_fill_color(230, 230, 230)  # Apply grey background to entire block
                    for code_line in code_block_lines:
                        self.multi_cell(0, 6, code_line, fill=True)
                    self.ln(5)
                    in_code_block = False
                    code_block_lines = []  # Reset for next block
                else:
                    # Start of code block
                    in_code_block = True
                    code_block_lines = []  # Initialize list for storing code block lines

            elif in_code_block:
                code_block_lines.append(line) # store the lines

            elif line.startswith("`"):  # Inline code (e.g., `code`)
                self.set_font("Courier", "", 11)
                self.set_fill_color(255, 255, 255)  # No background for inline code
                self.multi_cell(0, 6, line, fill=True)

            else:
                # Regular text (non-code block)
                self.set_font("Times", "", 12)
                self.set_fill_color(255, 255, 255)
                if line:  # non empty line
                    self.multi_cell(0, 6, line, fill=True)

        self.ln(5)
