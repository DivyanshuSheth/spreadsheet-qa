from openai import OpenAI
import argparse
import base64
from PIL import Image
import io
import os
import json
# from pydantic import BaseModel
from prompts import expert_prompt_template  # Importing the expert prompt template

# # Define the structured output schema using Pydantic
# class ImageResponse(BaseModel):
#     answer: str
#     category: str  # Adding category to the schema

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def load_image_as_base64(image_path):
    """
    Loads an image from the specified path and converts it to a base64 encoded string.
    
    :param image_path: Path to the image file.
    :return: Base64 encoded string of the image.
    """
    try:
        with Image.open(image_path) as img:
            buffered = io.BytesIO()
            img.save(buffered, format='PNG')
            img_b64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            return img_b64_str, 'image/png'
    except Exception as e:
        print(f"Error loading and encoding image: {e}")
        return None, None
    
def concatenate_images_vertically(images, output_dir):
    """
    Concatenates a list of images vertically.

    :param images: List of image paths.
    :return: Path to the concatenated image.
    """
    loaded_images = [Image.open(img) for img in images]
    
    total_height = sum(img.height for img in loaded_images)
    max_width = max(img.width for img in loaded_images)
    
    new_image = Image.new('RGB', (max_width, total_height))
    
    y_offset = 0
    for img in loaded_images:
        new_image.paste(img, (0, y_offset))
        y_offset += img.height
    
    concatenated_path = os.path.join(output_dir, 'concatenated_image.png')
    new_image.save(concatenated_path)
    
    return concatenated_path

def get_answer_from_gpt4o_with_image_b64(img_b64_str, img_type, question):
    """
    Gets an answer from GPT-4o given a base64 encoded image and a question.
    
    :param img_b64_str: The base64 encoded string of the image.
    :param img_type: The MIME type of the image.
    :param question: The question to ask.
    :return: Answer and category generated by GPT-4o.
    """
    # Format prompt with actual user question
    expert_prompt = expert_prompt_template.format(user_question=question)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": expert_prompt  # Use formatted expert prompt here
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"},
                    },
                ],
            }
        ],
        temperature=0.2  # Set temperature to 0.2
    )
    
    # Convert JSON string to dictionary
    # try:
    # only keep the content between the {} brackets
    answer_content = response.choices[0].message.content
    answer_content = answer_content[answer_content.find("{"):answer_content.rfind("}")+1]
    # print(response.choices[0].message.content)
    response_content = json.loads(answer_content)
    # except:
    #     print(response)
    
    
    # Extract answer and category from response
    # answer = response_content.get("answer", "")
    # category = response_content.get("category", "")
    
    return response_content


def main():
    parser = argparse.ArgumentParser(description='Question answering over images using GPT-4o.')
    parser.add_argument('--image_dir', type=str, required=True, help='Path to the directory containing images.')
    parser.add_argument('--question', type=str, required=True, help='The question to be answered.')

    args = parser.parse_args()

    print(f"Image Directory: {args.image_dir}")
    print(f"Question: {args.question}")

    # Get sorted list of image paths
    image_paths = sorted([os.path.join(args.image_dir, f) for f in os.listdir(args.image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    partial_images = []
    
    relevant_info_found = False
    incomplete_info_found = False

    for image_path in image_paths:
        print(f'\nProcessing image: {image_path}')
        
        # Load and encode the image as base64
        img_b64_str, img_type = load_image_as_base64(image_path)
        
        if not img_b64_str:
            print(f"Failed to load and encode the image: {image_path}")
            continue
        
        # Get answer from GPT-4o
        response_content = get_answer_from_gpt4o_with_image_b64(img_b64_str, img_type, args.question)
        
        # Extract answer and category from response content
        answer = response_content.get("answer", "")
        category = response_content.get("category", "")
        explanation = response_content.get("explanation", "")
        
        print(f"Answer: {answer}")
        print(f"Category: {category}")
        print(f"Explanation: {explanation}")
        
        if category.lower().lstrip().rstrip() == 'relevant info':
            print("Complete answer found. Skipping further processing.")
            relevant_info_found = True
            return
        
        if category.lower().lstrip().rstrip() == 'incomplete info':
            print("Partial answer found. Concatenating images for further analysis.")
            partial_images.append(image_path)
            incomplete_info_found = True
            
            if len(partial_images) == 3:
                break
    
    
    if not relevant_info_found and not incomplete_info_found:
        print("No relevant information found in the images.")
        return
    
    if not relevant_info_found and len(partial_images) > 0:
        concatenated_image_path = concatenate_images_vertically(partial_images, args.image_dir)
        print("Concatenated image created. Path: ", concatenated_image_path)
        
        # Load and encode the concatenated image as base64
        concat_img_b64_str, concat_img_type = load_image_as_base64(concatenated_image_path)
        
        if concat_img_b64_str:
            response_content = get_answer_from_gpt4o_with_image_b64(concat_img_b64_str, concat_img_type, args.question)
            answer = response_content.get("answer", "")
            category = response_content.get("category", "")
            explanation = response_content.get("explanation", "")
            
            print(f"Concatenated Answer: {answer}")
            print(f"Concatenated Category: {category}")
            print(f"Concatenated Explanation: {explanation}")
        return
    
    print("No relevant information found in the images.")

# Entry point for the script
if __name__ == "__main__":
    main()