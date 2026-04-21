# TA Project Automation

Python automation workflow for turning project briefs into AI-generated Word documents, then optionally uploading them to OneDrive and creating Asana tasks for review.

## Features

- Generates structured project plans from free-text briefs using OpenAI.
- Exports output as `.docx` using `python-docx`.
- Saves run metadata to `last_run.json` for downstream integrations.
- Uploads generated documents to OneDrive (via Microsoft Graph API).
- Creates Asana tasks and posts follow-up comments with document links.
- Includes a more resilient workflow engine with retries and fallback output.

## Project Structure

- `ai_document_generator.py` - interactive CLI to generate AI content and Word document.
- `onedrive_integration.py` - uploads generated document to OneDrive.
- `asana_integration.py` - creates Asana tasks and internal comments.
- `main_workflow.py` - runs the complete end-to-end flow.
- `robust_workflow.py` - retry-enabled workflow engine with input quality checks.
- `requirements.txt` - Python dependencies.

## Prerequisites

- Python 3.9+ recommended
- OpenAI API key
- (Optional) Asana personal access token and project ID
- (Optional) OneDrive access token and target folder ID

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

# Optional: Asana integration
ASANA_TOKEN=your_personal_access_token
ASANA_PROJECT_ID=your_project_id

# Optional: OneDrive integration
ONEDRIVE_ACCESS_TOKEN=your_token
ONEDRIVE_FOLDER_ID=root
```

Notes:
- If Asana credentials are missing, task creation is skipped.
- If OneDrive token is missing, upload returns a simulated link.

## Usage

### 1) Generate document only

```bash
python ai_document_generator.py
```

You will be prompted for:
- Project name
- Project brief text (submit with an empty line twice)

Output:
- A generated `.docx` file
- `last_run.json` containing metadata and AI output

### 2) Run full workflow (AI + OneDrive + Asana)

```bash
python main_workflow.py
```

Flow:
1. Generate document
2. Upload to OneDrive
3. Create Asana task
4. Add task comment with document link

### 3) Run robust workflow engine (advanced)

`robust_workflow.py` contains retry logic, input quality checks, and fallback generation. You can run its built-in quick test:

```bash
python robust_workflow.py
```

## Dependencies

- `openai`
- `python-docx`
- `requests`
- `python-dotenv`

## Troubleshooting

- `Brief too short` error: provide at least 50 characters in the project brief.
- OpenAI/API errors: verify `OPENAI_API_KEY` and internet connectivity.
- Asana `401/403`: check token scopes and project access.
- OneDrive upload failure: validate access token and folder ID format.

## Security Notes

- Do not commit `.env` with real credentials.
- Rotate tokens if they are accidentally exposed.

