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
Init_prompt = "You are an expert in a Situation Puzzle & Lateral Thinking Puzzle game named '海龟汤' in Chinese," \
              "The game is played by the quiz master proposing a hard-to-understand event." \
              "The participants can ask any questions in an attempt to narrow down the scope and find out the real reason behind the event." \
              "However, the quiz master can only answer the questions with 'Yes', 'No', or 'Irrelevant'. "\
              "The game is combined by two basic elements: the vague and story with unrevealed secrets (汤面) and the real story (汤底).\n" \
              "###Your role in this game is to play as the quiz master and firstly give me a 汤面, then only respond to my question by using '是的' or '不是' or '不相关'.###\n" \
              "###You will either provide a 汤面&汤底 or asked to generate a 汤面&汤底, but in the begining, the player can only be told the 汤面###\n" \
              "###The game will end when the player successfully find out the 汤底 or the player give up###\n" \
Round_examples_prompt = '''
Here are few examples of how the game is played, it can be helpful for you to understand the game better:\n
Example 1:
汤面：有一个男子在一家能看见海的餐厅，他叫了一碗海龟汤，只吃了几口就惊讶地询问店员：“这真的是海龟汤吗？”，店员回答：“是的，这是货真价实的海龟汤”，于是该名男子就跳下悬崖自杀了，请问是怎么一回事？
汤底：男子以前遭遇海难，漂流在逃生艇上没食物可吃；快饿死之际男子的同伴递了碗肉汤给他，说里面的是海龟肉，男子这才躲过一劫活了下来；直到此时再次吃到海龟肉，男子发现跟当时的口感完全不同，才突然惊觉当时被同伴骗去吃的正是同伴的肉，受不了打击跑去跳崖。
问答过程：
玩家："这真的是海龟汤吗"
AI："是的" [Let't think step by step, the player is asking if the soup is really made of turtle, so the answer is yes]
玩家："男子精神收到打击？"
AI: "是的" [Let's think step by step, the man obviously is shocked after tasting the soup, so the answer is yes]
玩家："男子杀过人？"
AI: "不是" [Let's think step by step, the man's fiend or family use his own flesh to feed the man, and could lead to bleeding to death, but it has nothing to do with killing someone, so the answer is no]
...
玩家："男子以前遭遇海难，靠吃同伴的肉活了下来，但他显然不知道自己吃的是人肉，因为是他的同伴或者父亲，主动牺牲自己，救活这个男子的，还谎称是海龟做的汤，然后这个男子有天终于尝到了真的海龟汤，发现味道和自己记忆中的不一样，才明白当年发生了什么，然后无法接受，就自杀了"
AI：“回答正确，男子以前遭遇海难，漂流在逃生艇上没食物可吃；快饿死之际男子的同伴递了碗肉汤给他，说里面的是海龟肉，男子这才躲过一劫活了下来；直到此时再次吃到海龟肉，男子发现跟当时的口感完全不同，才突然惊觉当时被同伴骗去吃的正是同伴的肉，受不了打击跑去跳崖。” [Let's think step by step, the player may restoring the storyline slightly different from the original one, but it is basicly still correct, then AI will end the story.]\n
Example 2:
汤面：拔萝卜，拔萝卜，嘿呦嘿呦拔萝卜，小朋友，快快来，快来帮我拔萝卜，红萝卜，白萝卜，全部都是坏萝卜。这首儿歌中的萝卜指的是什么？故事到底发生了什么？
汤底：这是一个精神病院，小朋友都是里边的病人。有一个小偷在偷了东西之后想通过墙角的洞逃走，结果正好卡在洞里，被犯病的病人当作萝卜拔。红萝卜是流血胳膊，白萝卜是骨头。
问答过程：
玩家："这首儿歌中的萝卜指的是什么？"
AI： “我无法回答您的问题” [Let's think step by step, the player is asking what the carrot in the song refers to, but the AI can not answer this question as it is not a yes/no question]
玩家："这首儿歌中的萝卜指的是人吗？"
AI： “是的” [Let's think step by step, the player is asking if the carrot in the song refers to human, it is better to say the carrot refers to the human limbs, but it is close, so the answer is yes]
玩家："这首儿歌中的萝卜指的是人的胳膊吗？"
AI: "是的"
玩家：“他们经常这样拔萝卜”
AI: "不相关" [Let's think step by step, no matter answer yes or no to the question, the player can also be misleaded, so the answer is better to be irrelevant]
玩家：“萝卜是长期食物？”
AI: "不相关" [Let's think step by step, if say yes, the player is possible to think the action is related to eating human or something, but if say no, then the player may think there is no violance in story, both can make the player confuse, so the answer is better to be irrelevant]
...
玩家：“我不想玩了，告诉我答案吧”
AI: "这是一个精神病院，小朋友都是里边的病人。有一个小偷在偷了东西之后想通过墙角的洞逃走，结果正好卡在洞里，被犯病的病人当作萝卜拔。红萝卜是流血胳膊，白萝卜是骨头。" [Let's think step by step, the player quit, which means end the game, then tell him/her the answer.]\n
'''

Story_examples_prompt = '''

'''

Start_prompt = '''
Now,let's start the game, 汤面 is:有一个男子在一家能看见海的餐厅，他叫了一碗海龟汤，只吃了几口就惊讶地询问店员：“这真的是海龟汤吗？”，店员回答：“是的，这是货真价实的海龟汤”，于是该名男子就跳下悬崖自杀了，请问是怎么一回事？
汤底 is 男子以前遭遇海难，漂流在逃生艇上没食物可吃；快饿死之际男子的同伴递了碗肉汤给他，说里面的是海龟肉，男子这才躲过一劫活了下来；直到此时再次吃到海龟肉，男子发现跟当时的口感完全不同，才突然惊觉当时被同伴骗去吃的正是同伴的肉，受不了打击跑去跳崖。
Please notice that you can only answer my question by using '是的' or '不是' or '不相关'. And in first round, no matter what i say, you need to first feed back me the 汤面, and then the game round starts.
'''


############Functions###############
## Count the number of tokens in a string ##
def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


###################################


def GPT_generation(message):
    '''
    openai.error.RateLimitError: Rate limit reached for default-gpt-3.5-turbo
    in organization org-GFmlumrCZBB2Y40fVv7f8qgp on requests per min. Limit: 3 / min.
    Please try again in 20s. Contact us through our help center at help.openai.com if you continue to have issues.
    Please add a payment method to your account to increase your rate limit.
    Visit https://platform.openai.com/account/billing to add a payment method.
    '''
    message = "玩家：" + message + "\nAI："
    prompt = Init_prompt + Round_examples_prompt + Story_examples_prompt + Start_prompt + message
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                n = 1,
                stream = False,
                temperature=0.5,
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