# OCR Marksheet Parser

Parse marksheet images into structured JSON using EasyOCR + an LLM-backed schema parser. The app provides a simple web UI and a JSON API.

## Features
- Upload a marksheet image and get structured candidate info, subjects, and results.
- OCR preprocessing: grayscale, perspective correction, illumination correction, and denoising.
- Schema-validated output with confidence scores for each extracted field.
- Optional GPU acceleration when CUDA is available.

## Project Structure
- `app.py`: Flask app with `/` UI and `/analyze` API.
- `main.py`: OCR + LLM parsing pipeline.
- `ocr.py`: EasyOCR extraction and post-processing.
- `preprocess.py`: Image preprocessing helpers.
- `data_model.py`: Pydantic schema for output.
- `templates/` and `static/`: UI assets.
- `marksheets/`: sample images.

## Requirements
- Python 3.10+ (recommended)
- Ollama running locally for the LLM provider
- Optional: CUDA-enabled GPU for faster OCR

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Environment Setup
Create a `.env` file (or copy from `.env.example`) and set any required provider variables. The current code uses the Ollama provider:

```
OLLAMA_API_KEY=your_key_if_needed
```

If your Ollama setup does not require an API key, you can leave it empty.

## Running the App
Start the Flask server:

```bash
python app.py
```

Open the UI in your browser:

```
http://127.0.0.1:5000
```

## API Usage
`POST /analyze` accepts a multipart form upload with field name `file`.

Example with curl:

```bash
curl -X POST http://127.0.0.1:5000/analyze \
  -F "file=@marksheets/marks_sheet_1.webp"
```

The response is a JSON object matching the schema below.

## Output Schema (Full)
Each extracted field uses a `Data` wrapper that includes `value` and `confidence`.

```json
{
  "candidate": {
    "name": { "value": "Jane Doe", "confidence": 0.92 },
    "mothersName": { "value": "Anita Doe", "confidence": 0.85 },
    "fathersName": { "value": "Ravi Doe", "confidence": 0.88 },
    "roll_no": { "value": 12345, "confidence": 0.94 },
    "registration_no": { "value": "REG-2024-001", "confidence": 0.9 },
    "dob": { "value": "2006-05-12", "confidence": 0.9 },
    "exam_year": { "value": 2024, "confidence": 0.93 },
    "board": { "value": "State Board", "confidence": 0.87 },
    "institution": { "value": "ABC Public School", "confidence": 0.9 }
  },
  "subjects": [
    {
      "subjectName": { "value": "Math", "confidence": 0.93 },
      "maxMarks": { "value": 100, "confidence": 1.0 },
      "obtainedMarks": { "value": 92, "confidence": 0.9 },
      "grade": { "value": "A", "confidence": 0.85 }
    }
  ],
  "result_summary": {
    "overallResult": { "value": "PASS", "confidence": 0.86 },
    "totalObtained": { "value": 465, "confidence": 0.88 },
    "percentage": { "value": 93.0, "confidence": 0.82 }
  },
  "meta_info": {
    "issueDate": { "value": "2024-06-30", "confidence": 0.77 },
    "placeOFIssue": { "value": "Jaipur", "confidence": 0.7 }
  }
}
```

## Notes on OCR and GPU
EasyOCR will use CUDA automatically if a GPU is available. If CUDA is not available, it runs on CPU.

## Troubleshooting
- If OCR is slow, consider enabling CUDA and verifying your GPU drivers.
- If the LLM call fails, ensure Ollama is running and the model name in `main.py` is available.
- If uploads fail, check that the `uploads/` folder is writable.

## License
Add your license information here.
