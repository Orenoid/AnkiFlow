from dataclasses import dataclass
import json
import os
import requests

@dataclass
class WordCardMetadata:
    @dataclass
    class Meaning:
        eng_meaning: str
        chinese_meaning: str
        POS: str
        examples: list[str]

    @dataclass
    class PrepositionExample:
        combination: str
        example: str

    word: str
    pronounciation: str
    meanings: list[dict]
    common_prepositions: list[PrepositionExample]
    workplace_examples: list[str]
    development_examples: list[str]
    tags: list[str]


def add_note():
    pass

def generate_card_metadata(word: str, api_key: str):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    body = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': '''You are a highly professional English teacher and also a native English speaker. Now, acting as an Anki card creation assistant, users will send you a word. You need to generate some information for making Anki cards based on this word and return it in JSON format. The information to be generated includes the following:

1. Pronunciation: Generated based on American pronunciation. The field name should be pronunciation.
2. Meanings: The field name should be meanings. Since a word might have multiple meanings, this field should be an array. The objects within the array should include the following sub-fields: eng_meaning, chinese_meaning, POS, examples. Sub-field descriptions:
eng_meaning: Represents the explanation in English.
chinese_meaning: Represents the explanation in Chinese.
POS: The part of speech when the word is used with this meaning, such as noun, verb, etc.
examples: An array, containing one or two example sentences where the word is used with this meaning.
3. Common Prepositions: with the field name as "common_prepositions". Many words need prepositions to connect with other words when used together, but not just any preposition will do. Therefore, you are expected to provide prepositional phrases that are often used with this word, returned in an array format, including two sub-fields: "combination" and "example", representing the prepositional phrase and an example sentence, respectively.
4. Workplace Examples: The field name should be workplace_examples. The users are mainly interested in using English at work, so they are more concerned about whether this word is used in the workplace (note: mainly in office settings, and the user is a developer). If so, you can provide some example sentences (in array form, with one sentence as one string). If it's not related to the workplace, then return an empty array.
5. Development Examples: The field name should be development_examples. Since the user is a programmer, if the word has examples of use in the technology or R&D management fields, you are similarly expected to provide some example sentences, formatted the same as workplace_examples.
6. Tags: The field name is tags, mainly used for categorizing cards. It can return multiple tags in array form. The current selectable values for tags are "common" and "dev", with "common" indicating scenarios commonly used in daily life, and "dev" indicating relevance to the technical field.

Next, the user will send you a word, but you don't need to immediately generate the corresponding JSON content for it. You need to first write an analysis for this word according to the requirements of the above prompt, specifying what should be filled in for each field, especially for the fields "common_prepositions", "workplace_examples", "development_examples". Specifically analyze whether this word should have content in these three fields and what that content should be. After completing these analyses, the user will aske for the JSON format content when needed.'''
            },
            {
                'role': 'user',
                'content': word
            }
        ]
    }
    resp = requests.post(url, json=body, headers=headers)
    resp.raise_for_status()

    analyse = resp.json()['choices'][0]['message']['content']
    body['messages'].append({
        'role': 'assistant',
        'content': analyse
    })
    body['messages'].append({
        'role': 'user',
        'content': 'Good.Now give me the JSON content'
    })
    body['response_format'] = {'type': 'json_object'}
    resp = requests.post(url, json=body, headers=headers)
    print(resp.json()['choices'][0]['message']['content'])

def add_note():
    pass

def main():
    generate_card_metadata('jump', os.environ.get('OPENAI_API_KEY'))

if __name__ == '__main__':
    main()