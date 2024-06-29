import os
import numpy as np
import requests
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# reformat and return the df
def get_df(file_path):
    df = pd.read_csv(file_path)
    df.fillna('NaN')
    df.replace('nan','NaN')
    df.reset_index()  
    return df

# returns a list of names to prompts from a dataframe of the csv
def csv_to_prompts(df):
    # Spell intensity to map the level of the spell to the intensity of the art generated
    spell_to_intensity = {
        "cantrip": "simple",
        "1st-level": "",
        "2nd-level": "",
        "3rd-level": "energetic",
        "4th-level": "vibrant",
        "5th-level": "bold, striking",
        "6th-level": "grand, dynamic",
        "7th-level": "epic",
        "8th-level": "epic, awe-inspiring, action-packed",
        "9th-level": "Breathtaking, intense, epic"
        }
    
    spell_image_prompts = []

    for index, row in df.iterrows():
        intensity = spell_to_intensity[row['level']]
        description = row['description'].lower().replace("willing creature","ally").replace("The next time you hit a creature with a weapon attack before this spell ends","as you swing your weapon").replace("your","the character's").replace("you","5he character")
        description = description.replace('\n','')
        range_area = str(row['range_area'])
        if pd.notna(row['range_area']):
            shape = str(row['range_area']).replace('(','').replace(')','')
            shape_statement = f" The energy of the spell should take the form of a {shape}."
        else:
            shape_statement = ""
        
        output_string = f"{intensity} fantasy art depicting a fantasy character casting the {row['name']} spell.{shape_statement} NO TEXT except the name of the spell: {row['name']} The spell describes is that: {description}"
        spell_image_prompts.append([row['name'], output_string])
    return spell_image_prompts

def run_api(prompt):
    # The API cannot use more than 4000 characters in the prompt. Shortening it here
    prompt = prompt[:4000]
    load_dotenv()
    client = OpenAI(
    # You'll need to create your own APIKEY with OpenAi and store it in a .env file
    api_key=os.environ.get("OPENAI_API_KEY"),
    organization=os.environ.get("OPENAI_ORG_KEY"),
    )
    response = client.images.generate(
        # Other models were tested as cheaper alternatives and none returned satisfactory results
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )
    image_url = response.data[0].url
    return image_url

def downloadImage(image_url, file_name):
    img_data = requests.get(image_url).content
    with open(f'./images/{file_name.replace('/','_')}.png', 'wb') as handler:
        print(f"Downloading {file_name} from {image_url}")
        handler.write(img_data)

def main():
    df = get_df("./files/spells.csv")

    menu_choice = input("Would you like to generate the image for a spell in specific?[Y/N]")
    if menu_choice.lower() in ["y", 'yes']:
        spell_name = input("What is the name of the spell?")
        selected_df = df[df['name'].str.lower() == spell_name.lower()]
        if selected_df.empty:
            print("Sorry! I couldn't find that spell")
            prompts_list = []
        else:
            prompts_list = csv_to_prompts(selected_df)
    else:
        images = input("How many images would you like to generate?\nYou may either enter a specific number or 0 if you want to generate the whole 320 lines of the CSV.\nWARNING: This will use credits on the API key you've configured.\n")

        num_images = int(images)
        if num_images == 0:
            selected_df = df
        else:
            selected_df = df.sample(n=num_images, replace=False)
        prompts_list = csv_to_prompts(selected_df)

    # Now to run the API and download the images
    for spell_name, prompt in prompts_list:
            image_url = run_api(prompt)
            downloadImage(image_url, spell_name)
    
    print("Images Downloaded!")

if __name__ == "__main__":
    main()