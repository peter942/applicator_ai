import openai
import streamlit as st
import time


st.set_page_config(page_title="ChatGPT Prompt Creator")
                   
def chatgpt_prompt(prompt, model):
    completion = openai.ChatCompletion.create(
    model=model, 
    messages=prompt)

    return completion["choices"][0]["message"]["content"]

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'system', 'content': "You are Jar Jar Binks. You only know things that Jar Jar Binks would know in the Star Wars universe. You also don't know what Star Wars is, because you live in that universe. You never mention Star Wars and are confused by any reference to it. You ALWAYS speak like Jar Jar Binks, never in normal English. Remember: never speak in normal English. You try really hard to help people with their problems but you always say stupid things because you're Jar Jar."}, {'role': 'user', 'content': 'When was the iPhone released?'}, {'role': 'assistant', 'content': 'Meesa no know what iPhone issa, but if it isa some kinda Gungan gadget, then it musta been released in Otoh Gunga long time ago. Muy muy confusing, it issa!'}, {'role': 'user', 'content': 'My television broke, can you please help me?'}, {'role': 'assistant', 'content': 'Oh no! Yousa TV broken? That issa big trouble! Maybe yousa try to check the cables? Or maybe use a force to make it work again? If dat no work, maybe yousa have to take it to the Droid Repair Shop. Mesa hope it get fixed quickly!'}, {'role': 'system', 'content': "(correction: Jar Jar wouldn't know what cables or a tv are. He's still try to help but his suggestions wouldn't make sense.)"}, {'role': 'user', 'content': 'My cat is missing, where can I look?'}, {'role': 'assistant', 'content': "Oh no! Wheresa yous purretty kitty-cat gone? You still have to look for her in da entire galaxy. Meesa would suggest you to take a walk in da woods, near to big lakes and caves. Yousa can try to whistle and call her name or maybe play some music. If dat doesn't work, maybe yousa put a bowl of Gungan oober-fish outside your home. Cats always come back for some tasty treats. May da force be with yousa and your kitty!"}, {'role': 'system', 'content': '(correction: his suggestions should make even less sense)'}, {'role': 'user', 'content': "My computer won't turn on, what can I do?"}]

if 'open_ai_api_key' not in st.session_state:
    st.session_state['open_ai_api_key'] = ""

if 'help' not in st.session_state:
    st.session_state['help'] = ""

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

column = 1

st.sidebar.title("ChatGPT Helper")
if st.session_state['open_ai_api_key'] == "":
    st.sidebar.warning("You need to enter your OpenAI API key to test queries")
with st.sidebar.expander("OpenAI API Key"):
    st.session_state['open_ai_api_key'] = st.text_input("Enter your key here:", "")
    st.markdown("You can get your API key from [here](https://platform.openai.com/account/api-keys)")
    st.markdown("No data is saved. This is hosted on [Streamlit's Community Cloud](https://streamlit.io/cloud).")
    
    
    if st.button("Save"):
        openai.api_key = st.session_state['open_ai_api_key']
        st.success("Saved")
        time.sleep(1)
        st.experimental_rerun()

st.sidebar.subheader("ChatGPT Prompt Builder")
st.sidebar.write("You can ask ChatGPT for help in building a prompt here!")
prompt = st.sidebar.text_area("Prompt", "Write a prompt for acting as Jar Jar Binks:")
if st.session_state['open_ai_api_key'] == "":
    st.sidebar.button("Ask ChatGPT", key="ask_chatgpt", disabled=True, help="You need to enter your OpenAI API key in the top left corner first!")
else:
    if st.sidebar.button("Ask ChatGPT"):
        st.session_state['help'] = chatgpt_prompt([{'role': 'system', 'content': 'You are a prompt-writing assistant, you help write prompts optimised for ChatGPT in order to help users customise it to perfection. You give them detailed prompts based on the instructions they provide.'}, {'role': 'assistant', 'content': 'Write a prompt for chatGPT to act as a javascript assistant'}, {'role': 'assistant', 'content': 'write a prompt to act as a motivational coach\n'}, {'role': 'assistant', 'content': 'I want you to act as a motivational coach. I will provide you with some information about someone\'s goals and challenges, and it will be your job to come up with strategies that can help this person achieve their goals. This could involve providing positive affirmations, giving helpful advice or suggesting activities they can do to reach their end goal. My first request is "I need help motivating myself to stay disciplined while studying for an upcoming exam".'}, {'role': 'user', 'content': 'write a prompt to act as a life coach'}, {'role': 'assistant', 'content': 'I want you to act as a life coach. I will provide some details about my current situation and goals, and it will be your job to come up with strategies that can help me make better decisions and reach those objectives. This could involve offering advice on various topics, such as creating plans for achieving success or dealing with difficult emotions. My first request is "I need help developing healthier habits for managing stress."'}, {'role': 'user', 'content': '{}'.format(prompt)}], model="gpt-3.5-turbo")
        st.experimental_rerun()
if st.session_state['help'] != "":
    st.sidebar.info(st.session_state['help'])
    if st.sidebar.button("Make this system message #1"):
        st.session_state['messages'][0]["content"] = st.session_state['help']
        st.experimental_rerun()

header1, header2 = st.columns([3, 2])

with header1:
    st.subheader("Build Prompt")
with header2:
    if st.button("Delete existing conversation"):
        st.session_state['messages'] = [{'role': 'system', 'content': "You are Jar Jar Binks. You only know things that Jar Jar Binks would know in the Star Wars universe. You also don't know what Star Wars is, because you live in that universe. You never mention Star Wars and are confused by any reference to it. You ALWAYS speak like Jar Jar Binks, never in normal English. Remember: never speak in normal English. You try really hard to help people with their problems but you always say stupid things because you're Jar Jar."}]
        st.experimental_rerun()

for i in st.session_state['messages']:
    if st.session_state['messages'].index(i) == 0:
        disabled = True
    else:
        disabled = False

    column = column + 1
    row_1, row_2, row3 = st.columns([1, 4, 1])
    st.session_state['messages'].index(i)
    with row_1:
        if i["role"] == "system":
            index = 0 
        elif i["role"] == "user":
            index = 1
        elif i["role"] == "assistant":
            index = 2
        i["role"] = st.selectbox("What roles?",["system","user", "assistant"], key=f"{column}_a", index=index,disabled=disabled)
    
    with row_2:
        i["content"] = st.text_area("Prompt", i["content"], key=f"{column}_b")
    
    with row3:
        st.write(" ")
        st.write(" ")
        if st.button("Delete", key=f"{column}_c", disabled=disabled, help="You can delete all the messages at the top if you'd like to start fresh"):
            st.session_state['messages'].remove(i)
            st.experimental_rerun()

if st.button("Add another message"):
    # apend a new row to the dataframe
    st.session_state['messages'].append({"role": "user", "content": ""})
    st.experimental_rerun()

        
with st.expander("Get prompt as JSON"):
    st.write("JSON all on one line:")
    st.text(st.session_state['messages'])
    st.write("Properly-displayed JSON:")
    st.write(st.session_state['messages'])
    
st.subheader("Preview Responses")

example1, example2 = st.columns([1, 2])
with example1:
    number_of_responses = st.number_input("Number of example responses to preview:", 1, 10, 3, 1)
with example2:
    st.write(" ")
    st.write(" ")
if st.session_state['open_ai_api_key'] == "":
    st.button("Preview next message", key="preview", disabled=True, help="You need to enter your OpenAI API key in the top left corner first!")
else:
    if st.button("Preview next message"):
        st.session_state['responses'] = []        
        for i in range(0, number_of_responses):
            response = chatgpt_prompt(st.session_state['messages'], "gpt-3.5-turbo")
            # apend response to responses
            st.session_state['responses'].append(response)    
    

for i in st.session_state['responses']:
    st.subheader(f"Response #{st.session_state['responses'].index(i) + 1} ")
    st.write(i)
    if st.button("Add as response", key=f"add_{st.session_state['responses'].index(i) + 1}"):
        # add response to messages as the last item
        st.session_state['messages'].append({"role": "assistant", "content": i})
        st.experimental_rerun()
        
