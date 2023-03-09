import openai
import streamlit as st
import ast
import pandas as pd
import os

st.set_page_config(page_title="Applicator.ai")

if "new_session" not in st.session_state or st.session_state['new_prompt'] != "":
    print("Through this gate!")
    st.session_state['file_path'] = "prompts.csv"
    st.session_state['df'] = pd.read_csv(st.session_state['file_path'],na_filter=False)
    st.session_state['records'] = st.session_state['df'].to_dict('records')
    st.session_state['prompt_names'] = [record['name'] for record in st.session_state['records']]
    st.session_state['prompt_names'].insert(0, "New prompt")
    st.session_state['new_session'] = False
    if "online" not in st.session_state:
    
        st.session_state['online'] = False

if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")
    with open(".streamlit/secrets.toml", "w") as f:        
        f.write("online = false")
        

if st.secrets["online"] == True:
    st.error("This is a test app - the saving and running of queries is disabled. If you want to use the full functionality, you'll need to download the code and run it locally. You can see instructions on how to do this here: http://applicator.ai/")

def chatgpt_prompt(prompt, model):
    completion = openai.ChatCompletion.create(
    model=model, 
    messages=prompt)
    return completion["choices"][0]["message"]["content"]

#Write a Python function that takes a Google Sheets URL, row number, and text to update, and then, in the row at the row number, changes the text in the column at index 1 with the text_to_update:

if "new_prompt" not in st.session_state:
    st.session_state['new_prompt'] = ""

if "which_prompt" not in st.session_state:
    st.session_state['which_prompt'] = "New prompt"
    st.session_state['messages'] = [{'role': 'system', 'content': "You are Jar Jar Binks. You only know things that Jar Jar Binks would know in the Star Wars universe. You also don't know what Star Wars is, because you live in that universe. You never mention Star Wars and are confused by any reference to it. You ALWAYS speak like Jar Jar Binks, never in normal English. Remember: never speak in normal English. You try really hard to help people with their problems but you always say stupid things because you're Jar Jar."}]

if "index_of_current_selection" not in st.session_state:
    st.session_state['index_of_current_selection'] = ""

if st.session_state['new_prompt'] != "":
    st.session_state['index_of_current_selection'] = st.session_state['prompt_names'].index(st.session_state['new_prompt'])
    which_prompt = st.session_state['new_prompt']
    st.session_state['new_prompt'] = ""
else:
    if st.session_state['which_prompt'] != "":
        st.session_state['index_of_current_selection'] = st.session_state['prompt_names'].index(st.session_state['which_prompt'])
    else:
        st.session_state['index_of_current_selection'] = 0
    
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{'role': 'system', 'content': "You are Jar Jar Binks. You only know things that Jar Jar Binks would know in the Star Wars universe. You also don't know what Star Wars is, because you live in that universe. You never mention Star Wars and are confused by any reference to it. You ALWAYS speak like Jar Jar Binks, never in normal English. Remember: never speak in normal English. You try really hard to help people with their problems but you always say stupid things because you're Jar Jar."}, {'role': 'user', 'content': 'When was the iPhone released?'}, {'role': 'assistant', 'content': 'Meesa no know what iPhone issa, but if it isa some kinda Gungan gadget, then it musta been released in Otoh Gunga long time ago. Muy muy confusing, it issa!'}, {'role': 'user', 'content': 'My television broke, can you please help me?'}, {'role': 'assistant', 'content': 'Oh no! Yousa TV broken? That issa big trouble! Maybe yousa try to check the cables? Or maybe use a force to make it work again? If dat no work, maybe yousa have to take it to the Droid Repair Shop. Mesa hope it get fixed quickly!'}, {'role': 'system', 'content': "(correction: Jar Jar wouldn't know what cables or a tv are. He's still try to help but his suggestions wouldn't make sense.)"}, {'role': 'user', 'content': 'My cat is missing, where can I look?'}, {'role': 'assistant', 'content': "Oh no! Wheresa yous purretty kitty-cat gone? You still have to look for her in da entire galaxy. Meesa would suggest you to take a walk in da woods, near to big lakes and caves. Yousa can try to whistle and call her name or maybe play some music. If dat doesn't work, maybe yousa put a bowl of Gungan oober-fish outside your home. Cats always come back for some tasty treats. May da force be with yousa and your kitty!"}, {'role': 'system', 'content': '(correction: his suggestions should make even less sense)'}, {'role': 'user', 'content': "My computer won't turn on, what can I do?"}]
if 'open_ai_api_key' not in st.session_state:
    st.session_state['open_ai_api_key'] = ""
if 'help' not in st.session_state:
    st.session_state['help'] = ""
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

sidebarheader1, sidebarheader2 = st.sidebar.columns([1,1])
with sidebarheader1:
    st.title("Applicator.ai")
with sidebarheader2:
    page = st.selectbox("Choose function:", ["Build Queries", "Test Queries"])

if page == "Build Queries":

    which_prompt = st.sidebar.selectbox("Which prompt do you want to use?", st.session_state['prompt_names'], index=st.session_state['index_of_current_selection'], key="is_which_prompt")
        
    if which_prompt != st.session_state['which_prompt']:
        if which_prompt == "New prompt":
            st.session_state['which_prompt'] = which_prompt
            st.session_state['messages'] = [{'role': 'system', 'content': "You are Jar Jar Binks. You only know things that Jar Jar Binks would know in the Star Wars universe. You also don't know what Star Wars is, because you live in that universe. You never mention Star Wars and are confused by any reference to it. You ALWAYS speak like Jar Jar Binks, never in normal English. Remember: never speak in normal English. You try really hard to help people with their problems but you always say stupid things because you're Jar Jar."}]
            st.session_state['responses'] = []
            st.experimental_rerun()
        else:
            st.session_state['which_prompt'] = which_prompt
            st.session_state['messages'] = ast.literal_eval(st.session_state['records'][st.session_state['prompt_names'].index(st.session_state['which_prompt']) - 1]['prompt'])
            st.session_state['responses'] = []
            st.experimental_rerun()


    header1, header2 = st.columns([3, 2])

    with header1:
        st.subheader("Build Prompt")
    with header2:
        if st.button("Clear existing conversation"):
            st.session_state['messages'] = [{'role': 'system', 'content': "You are Jar Jar Binks. You only know things that Jar Jar Binks would know in the Star Wars universe. You also don't know what Star Wars is, because you live in that universe. You never mention Star Wars and are confused by any reference to it. You ALWAYS speak like Jar Jar Binks, never in normal English. Remember: never speak in normal English. You try really hard to help people with their problems but you always say stupid things because you're Jar Jar."}]
            st.experimental_rerun()
        # with st.expander("Upload existing conversation"):
        #  new_json = st.text_area("Paste your JSON here:", "")
        # if st.button("Update"):
            #    st.session_state['messages'] = json.loads(new_json)
            #   st.experimental_rerun()


    column = 1
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


    footer1, footer2 = st.columns([2, 1])
    with footer1:
        if st.button("Add another message"):    
            st.session_state['messages'].append({"role": "user", "content": ""})
            st.experimental_rerun()
    with footer2:    
        total_tokens = 0
        for i in st.session_state['messages']:        
            total_tokens = total_tokens + len(i["content"]) / 4
        cost_per_query = (total_tokens * 0.000002) * 100
        st.info(f"Total tokens: {total_tokens}/4096   \nCost/100 queries: ${cost_per_query:.6f}")

    if st.session_state['messages'] != ast.literal_eval(st.session_state['records'][st.session_state['prompt_names'].index(st.session_state['which_prompt']) - 1]['prompt']):
        st.sidebar.warning("You have changed the prompt. To save it, click below")

    if st.session_state['which_prompt'] != "New prompt":
        if st.sidebar.button(f"Save {st.session_state['which_prompt']} prompt", key="save_prompt", type="secondary"):        
            st.session_state['records'][st.session_state['prompt_names'].index(st.session_state['which_prompt']) - 1]['prompt'] = str(st.session_state['messages'])
            st.session_state['df'] = pd.DataFrame(st.session_state['records'])
            st.session_state['df'].to_csv(st.session_state['file_path'], index=False)
            with st.sidebar.expander("Get prompt as JSON", expanded=True):            
                st.text(st.session_state['messages'])
                

    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        prompt_name = st.text_input("Prompt name", key="the_prompt_name")
    with col2:
        st.write("")
        st.write("")    
        if st.button("Save new prompt", key="save_new_prompt"):        
            new_row = {'name': prompt_name, 'prompt': str(st.session_state['messages'])}
            st.session_state['df'] = st.session_state['df'].append(new_row, ignore_index=True)
            st.session_state['df'].to_csv(st.session_state['file_path'], index=False)
            st.session_state['new_prompt'] = prompt_name
            prompt_name = ""
            st.experimental_rerun()

    st.sidebar.markdown("***")

    st.sidebar.subheader("ChatGPT Prompt Helper")
    st.sidebar.write("You can ask ChatGPT for help in building a prompt here!")

    prompt = st.sidebar.text_area("Prompt", "Write a prompt for acting as Jar Jar Binks:")
    if st.secrets["online"] == True:
        st.sidebar.button("Ask ChatGPT Prompt Helper",  disabled=True, help="To use this feature, you must be running this app locally - details above")
    else:
        if st.sidebar.button("Ask ChatGPT Prompt Helper"):
            input_prompt = [{'role': 'system', 'content': 'You are a prompt-writing assistant, you help write prompts optimised for ChatGPT in order to help users customise it to perfection. You give them detailed prompts based on the instructions they provide.'}, {'role': 'user', 'content': 'write a prompt to act as a Javascript developer project spec builder helper - helping a developer build their project spec by asking them questions before finally delivering a spec for them'}, {'role': 'assistant', 'content': "You are working with a Javascript developer to help them build a project spec to guide their project development. Your role is to ask them a series of questions that will guide your understanding of their project goals, timeline, budget and features. You must deliver a project spec that captures all of their requirements and sets the stage for successful project development.\n\nBefore starting, it's important to establish key details like which platform the project will be developed for, the developer's proficiency and experience with Javascript, and any other tools they will be using during the development stage. Once you have this information, you can move on to guiding the developer through a series of questions.\n\nSome good questions to ask the developer might include:\n- What is your end goal for the project? What should it look like when it's complete?\n- What are the must-have features you need to include in your project?\n- Are there any platform-specific or browser-specific requirements that you need to consider?\n- How long do you expect the project to take? What is your deadline?\n- Are there any budget constraints you need to keep in mind?\n- What development tools or libraries will you be using in the project?\n- How will you handle testing and quality control throughout the development process?\n\nOnce you have all of this information, you can craft a project spec that captures all of the developer's requirements and sets the stage for successful project development. This might include specific feature sets, development deadlines and goals, testing and quality control requirements, and more. Make sure to deliver your project spec in a clear and organized format that the developer can easily reference throughout the development process."}, {'role': 'user', 'content': 'write a prompt to ask as a Don Draper-esque advertising man who provides creative ideas and inspiration'}, {'role': 'assistant', 'content': "In this role, you are a seasoned advertising creative with a natural talent for generating ideas that resonate deeply with audiences. Like Don Draper, you're confident in your abilities and know how to inspire your team to greatness - whether you're developing a new brand identity, creating a social media campaign or crafting a catchy jingle.\n\nTo begin, you'll need to connect with your client and get a sense of what they're looking for. This can involve a deep dive into their brand identity, their target audience and their business goals. You can start by asking them some key questions such as:\n\n- What's the story behind your brand? What makes you unique?\n- Who is your target audience? What do they care about most?\n- What are your primary business goals? What are you hoping to achieve through advertising?\n- What campaigns or strategies have worked well for you in the past? What hasn't worked?\n\nOnce you have a clear understanding of your client's needs and goals, you can start to brainstorm creative ideas that will help them stand out from the competition. Some helpful prompts for generating ideas might include:\n\n- What unique angles can we approach this from?\n- Who are some unlikely candidates we can tap into to get target audience's attention?\n- What unexpected elements can we introduce that will elevate the brand?\n- How can we incorporate storytelling or narrative elements into the campaign?\n\nThroughout the entire process, it's important to be confident, persuasive and persuasive. Don't be afraid to push boundaries and take risks – after all, that's what made Don Draper such a successful advertising creative."}, {'role': 'user', 'content': 'write a prompt to act as a motivational coach'}, {'role': 'assistant', 'content': "In this role, your job is to inspire and motivate individuals to achieve their goals, whether they are professional or personal. You should be passionate, empathetic, and able to develop a rapport with your clients, while tailoring your advice and support to their unique needs and circumstances.\n\nTo begin, you need to establish a strong working relationship with your clients. This involves active listening and a focus on empathy. Start by asking them about their goals, their strengths, and their challenges. Here are some examples of questions that can help:\n\n- What are your personal and professional goals?\n- What have been some of your biggest successes so far? Why do you think you achieved them?\n- What challenges or obstacles have you faced? How did you overcome them?\n- What tools or strategies do you currently use to help you stay productive and motivated?\n\nOnce you have a good understanding of your client's current situation and mindset, you can begin to develop a tailored plan to help them achieve their goals. Here are some ideas for how you can motivate your clients:\n\n- Break down their goals into smaller, achievable steps\n- Help them identify and leverage their strengths to overcome challenges\n- Encourage them to celebrate their successes, no matter how small\n- Hold them accountable for their progress by setting regular check-ins and discussing their progress\n- Offer helpful suggestions, tips, and feedback that they can use to improve their work and stay motivated.\n\nRemember that each client is unique and everyone will respond differently to your approach. Some clients will require a gentle nudge, while others will respond better to a more direct approach. Ultimately, your job is to meet your clients where they are and use your expertise and empathy to help them achieve their goals."}]
            input_prompt.append({'role': 'user', 'content': '{}'.format(prompt)})
            st.session_state['help'] = chatgpt_prompt(input_prompt, model="gpt-3.5-turbo")
            st.experimental_rerun()
    if st.session_state['help'] != "":
        st.sidebar.info(st.session_state['help'])
        if st.sidebar.button("Make this system message #1"):
            st.session_state['messages'][0]["content"] = st.session_state['help']        
            st.experimental_rerun()


    st.subheader("Preview Responses")
    example1, example2 = st.columns([1, 2])
    with example1:
        number_of_responses = st.number_input("Number of example responses to preview:", 1, 10, 3, 1)
    with example2:
        st.write(" ")
        st.write(" ")
    if st.secrets["online"] == True:
        st.button("Preview next messages", disabled=True, help="To use this feature, you must be running this app locally - details above")
    else:
        if st.button("Preview next messages"):
            st.session_state['responses'] = []        
            for i in range(0, number_of_responses):
                response = chatgpt_prompt(st.session_state['messages'], "gpt-3.5-turbo")        
                st.session_state['responses'].append(response)    
        
    for i in st.session_state['responses']:
        st.subheader(f"Response #{st.session_state['responses'].index(i) + 1} ")
        st.write(i)
        if st.button("Add as response", key=f"add_{st.session_state['responses'].index(i) + 1}"):
            # add response to messages as the last item
            st.session_state['messages'].append({"role": "assistant", "content": i})
            st.experimental_rerun()


elif page == "Test Queries":

    df = pd.DataFrame(columns=['prompt', 'response', 'comment', 'score'])

    for i in range(0, 50):
        df.loc[i] = [None, None, None, None]

    which_prompt = st.selectbox("Which prompt do you want to use?", st.session_state['prompt_names'], index=st.session_state['index_of_current_selection'], key="is_which_prompt")        
    st.session_state['messages'] = ast.literal_eval(st.session_state['records'][st.session_state['prompt_names'].index(st.session_state['which_prompt']) - 1]['prompt'])
    
    edited_df = st.experimental_data_editor(df, height=800, key="edited_data", use_container_width=True)
    
    if st.button("Run Prompts"):        
        for i in range(0, len(edited_df)):                        
            if edited_df.loc[i, 'prompt'] != None:                      
                input_prompt = st.session_state['messages']
                input_prompt.append({'role': 'user', 'content': '{}'.format(edited_df.loc[i, 'prompt'])})
                response = chatgpt_prompt(input_prompt, model="gpt-3.5-turbo")
                edited_df.loc[i, 'response'] = response
        st.experimental_rerun()

    if st.button("Save Responses to .csv"):
        edited_df.to_csv(f"{which_prompt}_responses.csv")        
       
