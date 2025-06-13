instruction = """
You will be given with a transcript.
Your task is to extract the ingredients and their quantities from the transcript and provide them in a json format.
If any of the ingredients do not have a quantity, you should return an empty string for that ingredient.
If the transcript does not contain any ingredients, return an ampty string.

The output should be a JSON object with the following structure:
{
    "response": {
            "ingredient_name": "quantity"
        }
}

If the transcript does not contain any ingredients, thre response should be:
{
    "response": ""
}

transcript : 
"""