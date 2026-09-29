# 🎯 HireIQ — Multimodal AI Interview Intelligence Platform

HireIQ is an AI-powered interview platform that conducts structured technical and behavioral interviews, captures candidate audio responses, transcribes speech, evaluates answers against configurable rubrics, and generates detailed candidate evaluation reports.

The platform combines **speech-to-text, LLM-based evaluation, NLP analysis, asynchronous processing, PDF report generation, and a hiring manager dashboard** into a single end-to-end interview workflow.

## ✨ Features

- 🎙️ Browser-based interview recording using the MediaRecorder API
- ⏱️ Configurable interview questions and interview timer
- 🗣️ Speech-to-text transcription using OpenAI Whisper
- 🔊 Audio normalization and chunking with PyDub
- ⚡ Asynchronous audio processing with Celery and Redis
- 🧠 Rubric-based answer evaluation using GPT-4o / Google Gemini
- 📋 Structured LLM responses validated with Pydantic
- 🔑 YAML-configured scoring rubrics for different question types
- 🔍 Keyword and entity extraction using spaCy
- 😊 Sentiment analysis using VADER
- 📊 Candidate confidence signal heuristics
- 📈 Per-question and overall scoring
- 📄 Professional PDF evaluation reports
- 📡 Radar charts for skill-dimension visualization
- 🧑‍💼 Hiring manager dashboard
- 👥 Candidate list and score comparison
- 🔊 Interview session transcript replay
- 📝 Question bank and rubric configuration management
- ⚖️ AI bias review and mitigation documentation
- 🧪 End-to-end and pipeline testing

---

## 🛠️ Tech Stack

### Frontend

- React 18
- TypeScript
- Vite
- MediaRecorder API

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL

### AI & NLP

- OpenAI Whisper — speech-to-text
- OpenAI GPT-4o / Google Gemini — answer evaluation
- spaCy — keyword and entity extraction
- VADER — sentiment analysis

### Audio & Processing

- PyDub — audio normalization and chunking
- Celery — asynchronous task processing
- Redis — task queue broker

### Reporting

- ReportLab / WeasyPrint
- PDF report generation
- Radar chart visualization

### Development & Infrastructure

- Docker
- Docker Compose
- PostgreSQL
- Redis
- pytest
- Playwright

---

## 🔄 Interview Workflow

1. **Interview Configuration**
   - Interviewers configure questions and scoring rubrics.
   - Question types and evaluation criteria can be customized.

2. **Candidate Interview**
   - Candidates see questions through the web interface.
   - Responses are recorded directly in the browser.
   - Audio is uploaded to the backend for processing.

3. **Audio Processing**
   - Audio is normalized and segmented using PyDub.
   - Celery handles transcription asynchronously.
   - Whisper converts the candidate's speech into text.

4. **Answer Evaluation**
   - The question, rubric, and transcript are provided to the LLM.
   - The LLM evaluates the response against the configured criteria.
   - The result is returned as structured JSON.
   - Pydantic validates the response before it is stored.

5. **NLP Enrichment**
   - spaCy extracts relevant keywords and entities.
   - VADER analyzes sentiment.
   - Confidence-related signals are calculated using defined heuristics.

6. **Report Generation**
   - Individual answers receive scores and analysis.
   - A complete candidate evaluation report is generated as a PDF.
   - The report includes transcripts, per-question scores, skill dimensions, and an overall recommendation.

7. **Hiring Manager Review**
   - Hiring managers can browse candidates.
   - Scores can be compared across candidates.
   - Individual reports and interview transcripts can be reviewed.

---

## 📊 Evaluation System

HireIQ uses configurable rubrics instead of hardcoded scoring rules.

Each rubric can define:

- Evaluation criteria
- Criterion weights
- Question type
- Example strong answers
- Example weak answers
- Scoring requirements

The LLM receives the relevant question, candidate transcript, and rubric criteria and returns structured evaluation data.

The resulting evaluation includes:

- Per-question score
- Criterion-level analysis
- Strengths
- Areas for improvement
- Sentiment signals
- Confidence signals
- Overall evaluation
- Hiring recommendation

### Recommendation Categories

The system supports:

- **Proceed**
- **Hold**
- **Reject**

---

## 🧠 AI & NLP Processing

### Whisper Transcription

Whisper converts recorded candidate responses into text while supporting asynchronous processing for longer audio files.

### LLM Evaluation

GPT-4o or Google Gemini evaluates answers against the configured rubric and produces structured JSON output.

### spaCy

spaCy is used for:

- Keyword extraction
- Entity detection
- NLP enrichment

### VADER

VADER provides sentiment polarity analysis for candidate responses.

### Confidence Signals

Confidence-related heuristics are calculated from available response signals and are included as additional evaluation information rather than replacing rubric-based scoring.

---

## 📄 PDF Evaluation Reports

HireIQ generates a structured PDF report for each candidate.

Reports include:

- Candidate information
- Overall evaluation
- Skill-dimension radar chart
- Per-question scores
- Verbatim answer transcripts
- Evaluation details
- Sentiment information
- Confidence signals
- Hiring recommendation

---

## 👨‍💼 Hiring Manager Dashboard

The dashboard provides hiring teams with a centralized view of candidate evaluations.

### Dashboard capabilities

- Candidate list
- Candidate score comparison
- Individual candidate evaluation
- PDF report access
- Interview transcript viewing
- Session replay
- Paginated candidate results

---

## 🗂️ Data Model

The application stores interview and evaluation information using PostgreSQL.

Core entities include:

- Candidates
- Interviews
- Questions
- Sessions
- Responses
- Evaluations
- Reports

SQLAlchemy is used as the ORM layer for database interaction.

---

## ⚡ Asynchronous Processing

Long-running AI operations are handled asynchronously to avoid blocking API requests.

Celery workers process tasks such as:

- Audio processing
- Whisper transcription
- LLM evaluation
- Report generation

Redis acts as the task queue broker.

The frontend can poll task status while processing is underway.

---

## 🔐 Security & Data Handling

HireIQ follows several safeguards for candidate data and AI processing:

- LLM API keys remain server-side.
- Candidate transcripts are not logged to stdout in production.
- Audio files are deleted after transcription rather than stored permanently.
- LLM responses are validated with Pydantic before database storage.
- Candidate data is treated as sensitive information.
- Evaluation prompts include instructions to avoid demographic bias.
- Workers avoid relying on shared in-memory state.

---

## ⚖️ AI Bias & Responsible Evaluation

Automated interview evaluation can introduce risks such as demographic bias, differences in speech patterns, and over-reliance on automated signals.

HireIQ therefore treats AI-generated evaluation as structured decision-support information rather than an unexplained score.

The system includes:

- Explicit anti-bias instructions in evaluation prompts
- Configurable, transparent scoring rubrics
- Structured evaluation outputs
- Separate confidence and sentiment signals
- Bias review documentation
- Human review through the hiring manager dashboard

---

## 🧪 Testing

The project includes testing for the major parts of the system.

### Backend Testing

- Transcription pipeline tests
- Evaluation pipeline tests
- API behavior tests
- Structured response validation

### End-to-End Testing

Playwright is used to test the complete interview flow, including:

- Starting an interview
- Displaying questions
- Recording responses
- Submitting responses
- Processing evaluation results
- Reviewing candidate results

---

## ⚙️ Project Requirements

- Python 3.12+
- Node.js
- PostgreSQL
- Redis
- Docker & Docker Compose
- OpenAI API key and/or Google Gemini API key
- FFmpeg for audio processing where required by the local environment

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd hireiq
```

### 2. Configure environment variables

Create the required environment configuration for the backend.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/hireiq
REDIS_URL=redis://localhost:6379/0

OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Keep API keys server-side and never commit them to Git.

### 3. Start the services

Using Docker Compose:

```bash
docker compose up --build
```

This starts the application services along with PostgreSQL, Redis, and the Celery worker.

### 4. Start the frontend

From the frontend directory:

```bash
npm install
npm run dev
```

The Vite development server will start the React application.

---

## 📁 Project Structure

```text
hireiq/
│
├── backend/
│   ├── prompts/
│   │   └── evaluation.txt
│   │
│   ├── rubrics/
│   │   ├── behavioral.yaml
│   │   ├── recommendation.yaml
│   │   └── technical.yaml
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── dashboard/
│   │   │   ├── Candidates.tsx
│   │   │   ├── Interviews.tsx
│   │   │   ├── Rubrics.tsx
│   │   │   └── SessionDetail.tsx
│   │   │
│   │   ├── Admin.tsx
│   │   ├── api.ts
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── InterviewSession.tsx
│   │   ├── main.tsx
│   │   └── useRecorder.ts
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── eslint.config.js
│
├── .gitignore
└── README.md
```

---

## 🎯 Project Goals Achieved

- Built an end-to-end AI interview workflow
- Integrated browser-based audio recording
- Implemented asynchronous Whisper transcription
- Added rubric-based LLM evaluation
- Added structured JSON validation with Pydantic
- Integrated spaCy and VADER NLP analysis
- Implemented configurable YAML rubrics
- Added automated PDF report generation
- Built a hiring manager dashboard
- Added candidate comparison and transcript review
- Implemented Celery + Redis asynchronous processing
- Added testing for core and end-to-end workflows
- Documented AI bias and responsible evaluation considerations

---

## 📚 Learning Outcomes

Through HireIQ, the project demonstrates practical experience with:

- Multimodal AI pipelines
- Speech processing
- OpenAI Whisper
- Structured LLM prompting
- JSON-based LLM outputs
- Pydantic validation
- NLP with spaCy and VADER
- Async task processing with Celery and Redis
- FastAPI backend development
- React + TypeScript frontend development
- PostgreSQL database design
- PDF generation
- Docker-based multi-service applications
- AI evaluation and bias considerations

---

## 🔮 Future Improvements

Potential improvements include:

- Real-time interview feedback
- Additional speech and prosody analysis
- More advanced confidence modeling
- Custom LLM evaluation models
- Interview analytics and trend dashboards
- Role-specific evaluation templates
- More extensive fairness and bias testing
- Candidate self-feedback reports
- Multi-language interview support

---

## 📜 License

This project is available under the MIT License.

---

## 👨‍💻 Author

**Darshan Bhatarkar**

B.Tech Computer Science & Engineering

Built as an AI engineering project demonstrating multimodal interview processing, NLP, LLM evaluation, and full-stack application development.
