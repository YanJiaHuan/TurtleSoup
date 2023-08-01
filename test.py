import openai
import gradio as gr
import random
import time
import tiktoken

model_name = "gpt-3.5-turbo"
openai.api_key = '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'

#################model################
if model_name == "gpt-3.5-turbo":
    max_tokens_default = 4096
    price_input = 0.0015
    price_output = 0.002
    print(f'Model:{model_name}, max_tokens:{max_tokens_default},Price: ${price_input}/${price_output} for input/output')
elif model_name == "gpt-3.5-turbo-0613":
    max_tokens_default = 4096
    price_input = 0.0015
    price_output = 0.002
    print(f'Model:{model_name}, max_tokens:{max_tokens_default},Price: ${price_input}/${price_output} for input/output')
elif model_name == "gpt-3.5-turbo-16k":
    max_tokens_default = 16384
    price_input = 0.003
    price_output = 0.004
    print(f'Model:{model_name}, max_tokens:{max_tokens_default},Price: ${price_input}/${price_output} for input/output')
elif model_name == "gpt-3.5-turbo-0613-16k":
    max_tokens_default = 16384
    price_input = 0.003
    price_output = 0.004
    print(f'Model:{model_name}, max_tokens:{max_tokens_default},Price: ${price_input}/${price_output} for input/output')
else:
    print('model is not supported currently...')

############Prompt################




############Functions###############
## Count the number of tokens in a string ##
def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


###################################


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
                temperature=0.5,
                max_tokens=max_tokens_default,
                top_p = 1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response['choices'][0]['message']['content']

        except openai.error.RateLimitError as e:
            time.sleep(20)
            return "Rate limit reached. Please try again in 20s."

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])


    def respond(message, chat_history):
        bot_message = GPT_generation(message)
        money_spent = price_input * num_tokens_from_string(message) + price_output * num_tokens_from_string(bot_message)
        money_spent_response = f"Cost: ${money_spent:.4f}"
        chat_history.append((message, bot_message))
        chat_history.append(("Cost", money_spent_response))  # Display cost as a separate message from the bot
        time.sleep(2)
        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)