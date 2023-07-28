import gradio as gr
from transformers import pipeline
def greet(name):
    return "Hello " + name + "!"

pipe = pipeline('text-classification',model='distilbert-base-uncased-finetuned-sst-2-english', tokenizer='distilbert-base-uncased-finetuned-sst-2-english')
def clf(text):
    result = pipe(text)
    label = result[0]['label']
    score = result[0]['score']
    print(label, score)
    res = {label: score, 'Postive' if label == 'Negative' else 'Negative': 1 - score}
    return res
test_text = "是的，他有过出海的经历。"
print(clf(test_text))

demo = gr.Chatbot(fn=greet, inputs="text", outputs="text")
gr.close_all()
demo.launch(share=True)
