import openai
import gradio as gr
import random
import time

model_name = "gpt-3.5-turbo"
openai.api_key = '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'

def GPT_generation(prompt):
    '''
    openai.error.RateLimitError: Rate limit reached for default-gpt-3.5-turbo
    in organization org-GFmlumrCZBB2Y40fVv7f8qgp on requests per min. Limit: 3 / min.
    Please try again in 20s. Contact us through our help center at help.openai.com if you continue to have issues.
    Please add a payment method to your account to increase your rate limit.
    Visit https://platform.openai.com/account/billing to add a payment method.
    '''
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                n = 1,
                stream = False,
                temperature=0.0,
                max_tokens=600,
                top_p = 1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response['choices'][0]['message']['content']

        except openai.error.RateLimitError as e:
            time.sleep(20)
            return "Rate limit reached. Please try again in 20s."
        except Exception as e:
            return "Unexpected error. Please try again."

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        bot_message = GPT_generation(message)
        chat_history.append((message, bot_message))
        time.sleep(2)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)