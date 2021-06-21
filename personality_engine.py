import logging
import json
import os
from config import CONFIG
from pprint import pformat

logger = logging.getLogger("corpus.personality")

user_name = CONFIG["ai"]["name"]
personality_id = CONFIG["ai"]["personality"]

personality_file_name = "./personalities/" + personality_id + ".json"
with open(personality_file_name, "r") as f:
    personality_data = json.load(f)

personality_name = personality_data["name"]

logger.info("Using personality %s (%s)" % (personality_id, personality_name))

nl = "\n"
initial_prompt = f'''[The following is a chat conversation between {user_name} and {personality_name}.]
[{personality_data['description']}]
{nl.join(['[%s]' % sentence.replace('{{user}}', user_name).replace('{{name}}', personality_name) for sentence in personality_data['additional_information']])}

Example messages from {personality_name}:
###
User: sample message
{nl.join(['%s: %s' % (personality_name, sentence) for sentence in personality_data['example_messages']])}
User: sample message
###

'''

chat_buffer_file_name = "./conversations/" + os.path.basename(personality_file_name)
chat_buffer = []

def chat_buffer_to_string():
    return "\n".join([f"{data['name']}: {data['text']}" for data in chat_buffer])

def add_to_chat_buffer(name, txt):
    chat_buffer.append({"name": name, "text": txt})

def save_chat_buffer():
    with open(chat_buffer_file_name, "w") as f:
        json.dump(chat_buffer, f)

def load_chat_buffer():
    global chat_buffer
    if os.path.exists(chat_buffer_file_name):
        with open(chat_buffer_file_name, "r") as f:
            chat_buffer = json.load(f)

load_chat_buffer()

logger.debug("Initial prompt:\n" + initial_prompt)

generator = None

def set_generator(used_gen):
    global generator
    generator = used_gen

def user_conversation(txt):
    add_to_chat_buffer(user_name, txt)

    responses = []

    send_to_gen = chat_buffer_to_string() + "\n" + personality_name + ":"
    generations = generator.generate(send_to_gen, initial_prompt).splitlines()

    logger.debug(generations)
    
    responses.append(generations.pop(0).lstrip()) # Always a direct response.

    # for gen in generations[:2]:
    #     if not gen.startswith(personality_name + ":"): break
    #     responses.append(gen[len(personality_name) + 2:])

    for resp in responses: add_to_chat_buffer(personality_name, resp)

    save_chat_buffer()

    typing_resp = [(0 if ("typing_speed" not in personality_data or personality_data["typing_speed"] == 0) else (len(response) / personality_data["typing_speed"]), response) for response in responses]
    logger.debug("AI responses: %s", pformat(typing_resp))

    return typing_resp