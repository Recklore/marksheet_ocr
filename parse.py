import json
import instructor
from dotenv import load_dotenv

from ocr import ocr
from data_model import MarksheetData


load_dotenv()


def prepare_client(operator = "ollama", model="gpt-oss:120b-cloud"):

    system_prompt = """
    You are a document parser. I will provide OCR data in a JSON list format.
    Each item represents a detected text segment:
    - "text": The text content.
    - "confidence": The OCR confidence score (0.0 to 1.0).
    - "position": The position [x, y] coordinates of the text.

    YOUR GOAL:
    1. Use "position" to align subjects with their marks. Items with similar 'y' values are on the same row.
    2. Use "text" (confidence) to determine the reliability of the reading.
    3. Parse this into the required schema.
    """

    client = instructor.from_provider(operator + "/" + model)

    return client, system_prompt


def extract(client, system_prompt, ocr_data):

    responses = []
    for data in ocr_data:
        response = client.completions.chat.create(
            response_model=MarksheetData,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Here is the OCR data:\n{data}"}]
        )

        responses.append(response)

    return responses


def parse_marksheet(image_path):

    ocr_data = ocr(image_path)
    client, system_prompt = prepare_client()
    responses = extract(client, system_prompt, ocr_data)

    with open("responses.json", "w", encoding="utf-8") as f:
        
        json.dump([response.model_dump() for response in responses], f, indent=4, ensure_ascii=False)

        return f

if __name__ == "__main__":
    parse_marksheet()