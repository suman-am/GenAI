import os
import openai
from openai import AzureOpenAI
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Your OpenAI API key
#api_key = "YOUR_API_KEY"
client = AzureOpenAI(
    api_key="eb0713eed45149cf8e078b296985bd94",  
    api_version="2023-12-01-preview",
    azure_endpoint = "https://oaisodexo.openai.azure.com/"
    )

deployment_name= 'AI_USECASE'

# Initialize OpenAI API client
#openai.api_key = api_key

# Function to generate description mapping using ChatGPT
def generate_mapping(set_a_descriptions, set_b_descriptions):
    # Join descriptions from both sets
    descriptions = set_a_descriptions + set_b_descriptions

    # Prepare prompt for ChatGPT
    #prompt = "Description mapping between Set A and Set B:\n"
    #for desc in descriptions:
     #   prompt += f"Set A: {desc}\tSet B: ______\n"

    prompt = "Description mapping between Set A and Set B:\n"
    prompt1 = "Set A Description:\n"
    prompt2 = "Set B Description:\n"
    for desc in set_a_descriptions:
        prompt1 += f"Set A: {desc}"
    for desc in set_b_descriptions:
        prompt2 += f"Set B: {desc}"

    # Call ChatGPT to generate mappings
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "system", "content": "You are an AI assistant which will help us do the mapping between two files, first file is Set A and second file is Set B"},
                  {"role": "system", "content": "I am giving you the Set A desciptions now"},
                  {"role": "user", "content": prompt1},
                  {"role": "system", "content": "I am giving you the Set B desciptions now"},
                  {"role": "user", "content": prompt2},
                  {"role": "user", "content": prompt},
                  {"role": "system", "content": "Give me the output in table where you have mapped the set A description with set B description"}],
        max_tokens=1000,
        temperature = 0
    )
    print(response.choices[0].message.content)

    # Extract mappings from the response
    mappings = response.choices[0].message.content

    # Parse the mappings
    description_mapping = {}
    for idx, desc in enumerate(descriptions):
        mapping = mappings[idx].split(':')[-1].strip()
        description_mapping[desc] = mapping

    return description_mapping

# Function to handle file upload for Set A
def upload_set_a():
    file_path = filedialog.askopenfilename(title="Select Set A Excel File")
    if file_path:
        df_set_a = pd.read_excel(file_path)
        set_a_descriptions = df_set_a['Description_Set_A'].tolist()
        return set_a_descriptions
    return None

# Function to handle file upload for Set B
def upload_set_b():
    file_path = filedialog.askopenfilename(title="Select Set B Excel File")
    if file_path:
        df_set_b = pd.read_excel(file_path)
        set_b_descriptions = df_set_b['Description_Set_B'].tolist()
        return set_b_descriptions
    return None

# Function to display mapping in the UI
def display_mapping(set_a_descriptions, set_b_descriptions):
    description_mapping = generate_mapping(set_a_descriptions, set_b_descriptions)

    root = tk.Tk()
    root.title("Mapping Comparison")

    # Table to display Set A and Set B mapping
    table = tk.Text(root, height=10, width=60)
    table.pack()

    # Display mapping in the table
    table.insert(tk.END, "Set A\tSet B\n")
    for desc_a in set_a_descriptions:
        desc_b = description_mapping.get(desc_a, '')
        table.insert(tk.END, f"{desc_a}\t{desc_b}\n")

    root.mainloop()

# Function to initiate file uploads and display mapping
def start_mapping():
    set_a_descriptions = upload_set_a()
    set_b_descriptions = upload_set_b()

    if set_a_descriptions and set_b_descriptions:
        display_mapping(set_a_descriptions, set_b_descriptions)
    else:
        messagebox.showwarning("Error", "Please select both Set A and Set B Excel files")

# Create a Tkinter window for file uploads
root = tk.Tk()
root.title("Upload Excel Files")

upload_label = tk.Label(root, text="Upload Set A and Set B Excel files:")
upload_label.pack()

# Button to upload Set A file
upload_set_a_button = tk.Button(root, text="Upload Set A", command=upload_set_a)
upload_set_a_button.pack()

# Button to upload Set B file
upload_set_b_button = tk.Button(root, text="Upload Set B", command=upload_set_b)
upload_set_b_button.pack()

# Button to start mapping after uploading files
start_mapping_button = tk.Button(root, text="Start Mapping", command=start_mapping)
start_mapping_button.pack()

root.mainloop()
