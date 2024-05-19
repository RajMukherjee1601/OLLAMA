from flask import Flask, render_template, request, jsonify
import PyPDF2
import ollama

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    return get_chat_response(msg)

def get_chat_response(text):
    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()
        return text

    pdf_path = "thebook.pdf"
    all_text = extract_text_from_pdf(pdf_path)
    print(all_text)

    prompt_template1 = "YOU Are i poweful ai which an understand only the text which is given to you . The text is "
    prompt_template = "And answer the following question if the question doesnot found in the contain then provided ans not found in the document"
    question = text

    stream = ollama.chat(
        model='llama2',
        messages=[{
            'role': 'user',
            'content': f"{prompt_template1 + all_text + prompt_template + question}",
        }],
        stream=True,
        options={
            'temperature': 0.0
        }
    )

    response = ''
    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)
        response += chunk['message']['content']

    return response

if __name__ == '__main__':
    app.run()
