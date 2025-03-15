def gpt_summary(description, win_percentage='', amount_ratio=''):
    #imports
    import os
    import sys
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
    ###
    api_gpt=os.getenv('api_gpt')
    
    client = OpenAI(api_key=api_gpt)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": 'desc'+str(description) + 'win percentage' + win_percentage + 'ratio' +amount_ratio + ' This dataset represents the profit and loss of a strategy tell me how the strategy is doing and keep it one sentence and tell me if its profitable.'}
        ]
    )

    res_sum=completion.to_dict()['choices'][0]['message']['content']
    return res_sum

if __name__ == '__main__':
    gpt_summary()