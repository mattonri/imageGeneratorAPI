# Overview

This project uses the OpenAI DALL-E-3 API to generate images with prompts, built out of a csv file full of dnd spells. It handles building the prompts, sending them to the API and downloading the images afterward. If you wish to run the code, you will need your own paid openAI API key. 

This project was great to learn more about openAI APIs and image generators in general. I tested the prompts accross several different generators to iteratively improve them and it was interesting to see the differences between them.

[Software Demo Video](https://youtu.be/1CnUoN_NoPc)

# Development Environment

This program used Pandas and numpy to handle the data, requests to download the images and dotenv and openAI to communicate with the dall-e-3 API.

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference/introduction)
- [Dall-e-3 prompt tips and tricks](https://community.openai.com/t/dalle3-prompt-tips-and-tricks-thread/498040)

# Future Work

Overall I'm impressed with the quality of the images. Dall-e-3 has outperformed all of the online alternatives. That having been said, there are some minor changes I would like to make: 

- seperate important contextual elements from the full description of the spell to eliminate so much text in the images generated.
- Crop out text blocks from the images automatically.
- Input the images into a card format with the data from the CSV in a readable format.