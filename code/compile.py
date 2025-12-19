import re
import sys

def compile(raw_text: list[str], filename: str) -> str:
    return html_boilerplate(compile_core(raw_text), filename)

def compile_core(raw_text: list[str]) -> str:
    paragraphs = []
    buf = []
    for line in raw_text:
        if len(line.strip()) == 0:
            paragraphs.append('<br/>'.join(row[:-1] for row in buf))
            buf = []
        else:
            buf.append(compile_line(line))
    paragraphs.append('<br/>'.join(row[:-1] for row in buf))
    return ''.join([f'<p>{par}</p>' for par in paragraphs])

def compile_line(line: str) -> str:
    tooltip_pattern = re.compile(r'\[:(.*?)\|(.*?)\]')

    cleaned_line = clean_escapes(line)
    result = tooltip_pattern.sub(
        r'<span class="tooltip" data-tooltip="\1">\2</span>', 
        cleaned_line)
    return fix_escapes(result)

def clean_escapes(line: str) -> str:
    return (line.replace('\\\\', '%BACKSLASH%').replace('\\[', '%LBKT%')
            .replace('\\]', '%RBKT%').replace('\\|', '%PIPE%')
            .replace('\\n', '%NEWLINE%'))
        
def fix_escapes(line: str) -> str:
    return (line.replace('%BACKSLASH%', '\\').replace('%LBKT%', '[')
            .replace('%RBKT%', ']').replace('%PIPE%', '|')
            .replace('%NEWLINE%', '&#10;'))

def html_boilerplate(body: str, filename: str) -> str:
    return (
        f'<!doctype html><html><title>{filename}</title>' +
        f'<link rel="stylesheet" href="style.css" /></html><body>{body}</body>')

def main():
    if len(sys.argv) < 2:
        print("Usage: python compile.py in.txt out.html")
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        src = f.readlines()

    html_body = compile(src, input_file)
    with open(f'out/{output_file}', 'w', encoding='utf-8') as f:
        f.write(html_body)
    

if __name__ == "__main__":
    main()
