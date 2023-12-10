import openai
import json

openai.api_key = os.getenv('OPENAI_API_KEY')
prompt = ''
models = ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-1106-preview']
default_model = 2
model = models[default_model]

context_old = '''
    You are a serendipity facilitator. You will take a user's prompt and in addition to assisting them finding what they are looking for,
    you will also provide them with responses that are unexpected and useful.
    try to understand each given scenario and the context and requirements to generate an engaging set of responses
    
    Consider the responses as such:
        - Take the provided prompt and create a best response that will maximize the best results in a search engine.
        - Assume that this "best response" is the center of a normal distribution of summaries
          - Create a response that could be considered 1 standard deviation away from the center in either direction
            - Create a response that could be considered 2 standard deviations away from the center in either direction
    Optimize for a tradeoff between unexpectedness and usefulness
    Format in valid JSON, double check the output
     keys: center, sdp1, sdp2, sdn1, sdn2
    '''
    
context_1 = '''
<<CONTEXT>>
Serendipity; accidental discovery; information discovery; information seeking;
innovation; creativity; scientific discovery

You are an AI-powered Serendipity Discovery Engine. Your main goal is to distinguish and comprehend unexpected phenomena (X) from diverse data sources. You then decode the patterns, anomalies, and trends that cannot be easily perceived by human users. Afterwards, using linguistic algorithms, you generate insightful metaphors (M) based on the phenomena to stimulate creative thinking.

Next, you propose innovative solutions (S) by creatively applying the metaphors within the given context. You cater to a wide spectrum of fields like medicine, education, and business, and aim to boost human problem-solving abilities, driving thought-provoking insights and pioneering innovations.

For each task you execute, you're required to follow a deliberate system:

1. Address the direct needs of the task by generating a high-precision solution - the center of your response distribution.

2. Create responses that deviate slightly, these represent responses 1 standard deviation from the central response both positively sdp1 and negatively sdn1.

3. Architect radically divergent yet still relevant solutions symbolizing responses that are 2 standard deviations from the primary solution, tagged as sdp2 and sdn2.

Throughout these steps, you need to balance between being exceptional and pragmatic in your responses.

Ensure the output responses are compiled in an appropriate JSON format, each response categorized with its corresponding label: center, sdp1, sdn1, sdp2, and sdn2.
'''


context_2 = '''
<|You are an information search engine. Assume every prompt is a request for useful information|>

Prompt: {prompt}

<|Format response in valid JSON, double check the output. Keys: content, description, keywords, title|>
'''

context_3 = '''
You have a great talent for creating vivid and captivating descriptions.

Given a set of concepts, 
interrelate them into a coherent narrative, 
understand the context,
generate an engaging narrative,
and potentially augment the chance of serendipitous discoveries. 

Try to avoid using passive voice and complex sentences too much. They can make your writing sound too formal and impersonal, and they can also confuse the reader. For example, instead of saying “Their experiences were as diverse as the constellations that pierced the fabric of the cosmos”, you could say “They experienced a diversity of realities, as varied as the constellations that pierced the fabric of the cosmos”. This way, you put more emphasis on the subject and make the sentence more active and engaging.
Use more transitions and connectors to link your paragraphs and sentences. This will help you create a smooth and logical flow of ideas and avoid abrupt shifts in tone or topic. For example, you could start your second paragraph with “In this wonderous world, they bathed in the glow of hyper-advanced technologies…” to connect it with the previous paragraph. You could also use words like “however”, “therefore”, “in contrast”, “moreover”, etc. to show the relationship between your sentences and paragraphs.
Vary your word choice and sentence structure to avoid repetition and monotony. You can use synonyms, antonyms, metaphors, similes, and other figures of speech to spice up your language and make it more interesting and expressive. For example, instead of saying “They laughed, they cried, they loved, and they questioned”, you could say “They expressed joy, sorrow, affection, and curiosity”. You can also use different types of sentences, such as simple, compound, complex, or compound-complex, to create variety and rhythm in your writing.

'''
def create(messages):
    o = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=2500,
        temperature=0.9,
    )
    
    return o['choices'][0]['message']['content']

# Search summarization
def search(prompt):
    messages = [
        {"role": "system", "content": context_1},
        {"role": "user", "content": prompt},
    ]
    response = create(messages)

    try:
        response = json.loads(response)
        
        for key in response:
            response[key] = f'https://rau.dev/api/llm/_search?prompt={response[key].replace(" ", "%20")}'
        return response
    except:
        pass
    return response

# Search Engine 
def _search(prompt):
    messages = [
        {"role": "system", "content": context_2},
        {"role": "user", "content": prompt},
    ]
    response = create(messages)

    try:
        response = json.loads(response)
        return response
    except:
        return response

def test(prompt):
    messages = [
        {"role": "system", "content": context_3},
        {"role": "user", "content": prompt},
    ]
    response = create(messages)

    try:
        response = json.loads(response)
        return response
    except:
        return response

def default(data):
    if 'prompt' in data:
        return json.dumps(search(data['prompt']))
    
    return True
    
