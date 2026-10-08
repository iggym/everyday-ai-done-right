"""Batch B (2026-10): whisper.cpp (MIT) transcription and Tesseract / OCRmyPDF (Apache-2.0 / MPL-2.0) guides."""

WHISPER_SRC = "https://github.com/ggml-org/whisper.cpp"
WHISPER_TOOL = "whisper.cpp (local speech-to-text, MIT-licensed)"
WHISPER_FAMILY = "Open Source (whisper.cpp)"
TESS_SRC = "https://github.com/tesseract-ocr/tesseract"
TESS_TOOL = "Tesseract OCR (Apache-2.0)"
TESS_FAMILY = "Open Source (Tesseract OCR)"
OCRMY_SRC = "https://github.com/ocrmypdf/OCRmyPDF"
OCRMY_TOOL = "OCRmyPDF + Tesseract (MPL-2.0 / Apache-2.0)"
OCRMY_FAMILY = "Open Source (OCRmyPDF)"
LOCAL_FREE = "$0 — open-source licence, runs on your computer"
LOCAL_LIMIT = "Speed depends on your hardware; no quota or account"

WHISPER_STEPS_SETUP = (
    "Build whisper.cpp from the repository (follow its README for CMake steps), then download a model with the "
    "bundled script, for example <code>./models/download-ggml-model.sh base.en</code>. Models download once; transcription runs offline."
)
WHISPER_CONVERT = (
    "Convert your recording to 16 kHz mono WAV: <code>ffmpeg -i input.m4a -ar 16000 -ac 1 -c:pcm_s16le audio.wav</code>."
)

GUIDES = [
    {
        "slug": "whisper-cpp-meeting-transcripts-offline",
        "title": "Transcribe Meetings Offline with whisper.cpp",
        "hook": "Get accurate meeting transcripts from your own recordings on your own laptop, with nothing uploaded to a transcription service.",
        "category": "business", "tool": WHISPER_TOOL, "family": WHISPER_FAMILY, "source": WHISPER_SRC,
        "tags": ["transcription", "meetings", "whisper", "offline", "business"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Meeting audio often contains client names, pricing, and staff matters. whisper.cpp is an open-source port of OpenAI's Whisper speech model that runs entirely on your device, so the recording never has to leave the room.",
        "steps": [
            ("Set up whisper.cpp", WHISPER_STEPS_SETUP),
            ("Convert the recording", WHISPER_CONVERT),
            ("Transcribe", "Run the bundled command-line binary on the WAV file with the model you downloaded, and save the output as text. Check the README for the current binary name and flags."),
            ("Add speaker labels by hand", "Whisper does not reliably separate speakers. Use a two-minute pass to label the people who spoke, then keep the file."),
            ("Extract action items", "Paste the transcript into a local model (see the Ollama guides in this directory) and ask for owners and deadlines, then check each one against the audio."),
        ],
        "prompt": "From this meeting transcript, list: decisions made, action items with owner and due date (write 'unassigned' if unclear), open questions, and figures mentioned with the exact sentence they came from. Do not infer anything not said.\n\nTRANSCRIPT:\n<paste>",
        "checks": ["The transcript was produced without uploading audio", "Action items match a timestamp you have listened to", "Names and figures were checked against the recording"],
        "pitfalls": ["Background noise and crosstalk lower accuracy; use a clip-on microphone when you can.", "Recording a meeting may require consent under local law. Tell participants first."],
    },
    {
        "slug": "whisper-cpp-lecture-notes-offline",
        "title": "Turn Lecture Recordings into Captioned Study Notes Offline",
        "hook": "Transcribe a recorded lecture on your own machine, then turn it into structured study notes you can search, with no transcription subscription.",
        "category": "learning", "tool": WHISPER_TOOL, "family": WHISPER_FAMILY, "source": WHISPER_SRC,
        "tags": ["lectures", "study-notes", "transcription", "whisper", "learning"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Many courses record lectures, and re-listening is slow. A transcript you can search turns an hour of audio into minutes of review.",
        "steps": [
            ("Set up whisper.cpp", WHISPER_STEPS_SETUP),
            ("Convert and transcribe", WHISPER_CONVERT + " Then run the transcription binary and keep the timestamps in the output."),
            ("Generate notes from the transcript", "Use the prompt below in a local model, one lecture at a time."),
            ("Link notes back to timestamps", "Keep the [00:12:31] markers so you can jump to the exact point in the audio when you revise."),
            ("Review with your own words", "Rewrite three key ideas per lecture without looking at the notes. That is the step that builds memory."),
        ],
        "prompt": "Turn this lecture transcript into study notes: a title, five key ideas as bullets with the timestamp they start at, three terms with plain-English definitions taken from the lecture, and two questions a student should be able to answer afterwards. Do not add facts that are not in the transcript.\n\nTRANSCRIPT:\n<paste>",
        "checks": ["Timestamps match the audio", "Definitions come from the lecture, not from memory of the subject", "You can explain each key idea without the notes"],
        "pitfalls": ["Check recording rules with your instructor or institution before recording a class.", "Technical terms are often misheard; correct them against the slides."],
    },
    {
        "slug": "whisper-cpp-interview-practice-offline",
        "title": "Practise Interview Answers and Get a Transcript Without Uploading",
        "hook": "Record yourself answering practice questions, transcribe locally, and review your pace and filler words without sending your voice to a server.",
        "category": "career", "tool": WHISPER_TOOL, "family": WHISPER_FAMILY, "source": WHISPER_SRC,
        "tags": ["interview", "practice", "transcription", "whisper", "career"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Hearing yourself is uncomfortable and useful. A local transcript lets you count filler words, measure answer length, and check whether your examples have a clear result.",
        "steps": [
            ("Pick five likely questions", "Use the questions for your role and write them on cards."),
            ("Record each answer", "Answer aloud for about two minutes per question, with your phone on a table, and save each file."),
            ("Transcribe locally", WHISPER_CONVERT + " Then run whisper.cpp on each file. " + WHISPER_STEPS_SETUP),
            ("Score the transcript", "Count filler words (um, like, you know), note the number of seconds before your first point, and check that each answer has a result."),
            ("Re-record the weakest answer", "Improve one answer per session rather than rewriting all five."),
        ],
        "prompt": "Review this practice interview answer. Report: word count, filler words with counts, whether there is a clear situation, action, and result (quote where each is), and one suggestion to shorten it. Do not rewrite the answer for me.\n\nANSWER TRANSCRIPT:\n<paste>",
        "checks": ["Each answer includes an outcome you can verify", "Filler-word counts were checked by ear on one recording", "Your examples are true and can be discussed in depth"],
        "pitfalls": ["Do not memorise scripted answers word for word; aim for structure and confidence.", "A transcript cannot judge tone or body language. Also record a short video once in a while."],
    },
    {
        "slug": "whisper-cpp-family-captions-offline",
        "title": "Caption Family Videos and Voice Messages Locally",
        "hook": "Add readable captions and searchable transcripts to family videos and voice notes on your own computer, which helps relatives who are deaf or hard of hearing.",
        "category": "accessibility", "tool": WHISPER_TOOL, "family": WHISPER_FAMILY, "source": WHISPER_SRC,
        "tags": ["captions", "accessibility", "family", "whisper", "offline"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Captions make family videos usable for relatives who are deaf or hard of hearing, and they make voice notes searchable years later. The transcript stays on your computer.",
        "steps": [
            ("Extract the audio", "Use ffmpeg to pull the audio track: <code>ffmpeg -i video.mp4 -ar 16000 -ac 1 -c:pcm_s16le audio.wav</code>."),
            ("Transcribe", "Run whisper.cpp with the model you downloaded. Ask for timestamped output so each line has a start time."),
            ("Turn the transcript into captions", "Convert the timed text to an SRT subtitle file using a plain-text editor or a small script, then check the timings."),
            ("Burn in or attach", "Load the SRT as a sidecar file in most video players, or add it to the video with ffmpeg if you want it always visible."),
            ("Correct names", "Family names and place names are the most common errors. Fix them before you share."),
        ],
        "prompt": "Clean up this timed transcript for subtitles: keep each caption under two lines and 42 characters per line, correct obvious mishearings only when the context is clear, mark unclear words as [unclear], and keep the timestamps unchanged.\n\nTRANSCRIPT:\n<paste>",
        "checks": ["Captions are readable at the video's speed", "Family and place names are correct", "Unclear speech is marked rather than guessed"],
        "pitfalls": ["Speech models struggle with overlapping voices and music; expect to edit.", "Share private family recordings only with people you choose."],
    },
    {
        "slug": "whisper-cpp-travel-voice-journal",
        "title": "Turn Voice Notes from a Trip into a Searchable Travel Journal",
        "hook": "Record short voice memos on the road, transcribe them on your laptop later, and end up with a dated journal you can search for the restaurant name you forgot.",
        "category": "travel", "tool": WHISPER_TOOL, "family": WHISPER_FAMILY, "source": WHISPER_SRC,
        "tags": ["travel", "journal", "voice-notes", "whisper", "offline"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Voice notes are the fastest way to capture a trip. Transcribing them offline means you do not need roaming data or a paid journaling app to make them searchable.",
        "steps": [
            ("Record with dated filenames", "Use your phone's voice recorder and keep the default timestamp in the filename."),
            ("Batch the files at home", "Copy the audio to one folder and convert each file to 16 kHz WAV, as in the other whisper.cpp guides."),
            ("Transcribe the folder", "Run whisper.cpp once per file. Save each transcript next to its audio, with the same name."),
            ("Compile a day summary", "Use the prompt below in a local model, one day at a time, to make a readable diary entry."),
            ("Add the place names", "Keep a short list of places and check spellings from receipts or maps."),
        ],
        "prompt": "Turn these voice-note transcripts from one day into a short travel diary entry in the first person. Keep the order of events, include place names exactly as spoken, and keep it under 300 words. Do not add events or feelings that are not in the notes.\n\nNOTES:\n<paste>",
        "checks": ["Place names match your receipts or maps", "No events were added that you did not record", "Each entry is dated"],
        "pitfalls": ["Recording people without consent can be illegal in some places; ask first.", "Save the original audio too; the transcript is only a search index."],
    },
    {
        "slug": "tesseract-receipts-to-csv",
        "title": "Turn Paper Receipts into a CSV with Free Tesseract OCR",
        "hook": "Scan a shoebox of receipts with an open-source OCR engine on your own computer and export one spreadsheet-ready CSV for your budget.",
        "category": "household", "tool": TESS_TOOL, "family": TESS_FAMILY, "source": TESS_SRC,
        "tags": ["receipts", "ocr", "budget", "tesseract", "spreadsheet"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Receipts fade, and expense apps charge monthly fees. Tesseract is a free, open-source OCR engine that reads printed text well. A short script and a spreadsheet are enough to turn a folder of photos into a budget.",
        "steps": [
            ("Photograph flat and well lit", "Place each receipt on a dark surface, shoot from above, and save as PNG or JPG."),
            ("Install Tesseract", "Use your package manager (for example <code>brew install tesseract</code> or your Linux repository) and check with <code>tesseract --version</code>."),
            ("Extract the text", "Run <code>tesseract receipt.png stdout -l eng</code> for each photo and save the output to a text file per receipt."),
            ("Pull out the fields", "Ask a local model, or a short script, to extract date, merchant, total, and category into CSV columns. Use the prompt below."),
            ("Reconcile the total", "Check the extracted total against the printed total for every receipt. Fix the ones that differ."),
        ],
        "prompt": "From this OCR text of one receipt, return one CSV line with the columns: date (YYYY-MM-DD), merchant, total (numbers only, dot as decimal), currency, category (food, transport, household, health, other). If a field is not clear, write UNCLEAR in that cell. Output the header line once, then one data line.\n\nOCR TEXT:\n<paste>",
        "checks": ["Each total matches the printed receipt", "Dates are in one format", "UNCLEAR cells were fixed by hand"],
        "pitfalls": ["Thermal receipts fade over time; scan them soon after you get them.", "OCR confuses 0/O and 1/l. Check any total that looks wrong."],
    },
    {
        "slug": "ocrmypdf-scanned-forms-searchable",
        "title": "Make Scanned Forms Searchable with OCRmyPDF",
        "hook": "Turn a scanned council, benefits, or school form into a searchable PDF on your own computer, so you can find the reference number in seconds.",
        "category": "civic", "tool": OCRMY_TOOL, "family": OCRMY_FAMILY, "source": OCRMY_SRC,
        "tags": ["ocr", "pdf", "forms", "civic", "offline"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Government and school paperwork often arrives as scans. OCRmyPDF adds a text layer to the PDF using Tesseract, so you can search, copy, and paste from it without uploading anything.",
        "steps": [
            ("Install OCRmyPDF", "Follow the project's install guide for your system. It needs Tesseract and Ghostscript, which the guide lists."),
            ("Run it on one form", "Use <code>ocrmypdf --language eng scan.pdf searchable.pdf</code>. Use <code>--skip-text</code> if some pages already have text."),
            ("Check the result", "Search for a word you know is on the form. If it is not found, rescan at higher resolution and repeat."),
            ("Save the reference numbers", "Copy the reference, case number, or deadline into your calendar or a notes file the same day."),
            ("Keep originals", "Store the scan and the searchable copy together, with a date in the filename."),
        ],
        "prompt": "From the text of this official form, list: the issuing office, any reference or case number, every deadline with its date, the documents the form asks me to provide, and the contact details. Quote each item exactly. Do not interpret the legal effect of the form.\n\nFORM TEXT:\n<paste>",
        "checks": ["The reference number matches the printed form", "Every deadline is in your calendar", "The original scan is kept alongside the searchable copy"],
        "pitfalls": ["Poor scans give poor text; use 300 dpi or higher if you can.", "If a deadline matters, confirm it with the issuing office."],
    },
    {
        "slug": "tesseract-lab-printout-text-local",
        "title": "Read Lab Printouts Locally: Extract the Text, Then Prepare Better Questions",
        "hook": "Use open-source OCR to pull the text from a paper lab report, then prepare clearer questions for your clinician without uploading results to a cloud chatbot.",
        "category": "health", "tool": TESS_TOOL, "family": TESS_FAMILY, "source": TESS_SRC,
        "tags": ["health", "lab-results", "ocr", "tesseract", "privacy"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "Lab reports are dense. Extracting the text locally lets you search for a test name and write down questions in your own words. It does not replace the explanation your clinician gives you.",
        "steps": [
            ("Scan or photograph the report", "Flatten it, avoid glare, and save as PNG."),
            ("Extract the text", "Run <code>tesseract report.png stdout -l eng</code> and save the output to <code>report.txt</code>."),
            ("Check every number", "Compare numbers and units with the paper. OCR often misreads decimals and minus signs."),
            ("Write questions, not conclusions", "Use the prompt below to list the tests, the reference ranges printed on the report, and questions to ask."),
            ("Bring the list to your appointment", "Ask the clinician what each result means for you specifically."),
        ],
        "prompt": "From this lab report text, list each test name, its result, its units, and the reference range printed on the report. Mark any result the report itself flags as high or low. Then write up to five neutral questions a patient could ask a clinician. Do not interpret the results or give advice.\n\nREPORT TEXT:\n<paste>",
        "checks": ["Each value and unit matches the paper report", "No interpretation or advice was added", "Questions are written in your own words before the visit"],
        "pitfalls": ["Never change a medication or treatment based on a model's reading of your results.", "Urgent symptoms need immediate medical care, not a spreadsheet."],
    },
    {
        "slug": "ocrmypdf-screen-reader-scans",
        "title": "Make Scanned Documents Work with Screen Readers Using OCRmyPDF",
        "hook": "Add a real text layer to scanned letters and handouts so screen readers, zoom, and copy-paste all work, without paying for OCR software.",
        "category": "accessibility", "tool": OCRMY_TOOL, "family": OCRMY_FAMILY, "source": OCRMY_SRC,
        "tags": ["accessibility", "screen-reader", "ocr", "pdf", "offline"],
        "free": LOCAL_FREE, "limits": LOCAL_LIMIT,
        "intro": "A scan is just a picture of text to a screen reader. Adding a text layer makes the same document readable aloud, searchable, and enlargeable without losing layout.",
        "steps": [
            ("Scan at 300 dpi", "Greyscale is fine; colour is only needed for diagrams."),
            ("Run OCRmyPDF", "Use <code>ocrmypdf --language eng --deskew scan.pdf accessible.pdf</code>. <code>--deskew</code> straightens crooked pages and improves recognition."),
            ("Test with a screen reader", "Open the file in your screen reader or the built-in reader and listen to the first page."),
            ("Fix the tags if needed", "For complex forms, a tagged PDF editor may be required; note this for later."),
            ("Provide an alternative when necessary", "For maps or charts, add a plain-text description next to the document."),
        ],
        "prompt": "Write concise alt text for each figure described in the notes below. Keep each description under 40 words, say what matters for understanding the document, and do not invent details.\n\nNOTES ON FIGURES:\n<paste>",
        "checks": ["Text can be selected and read aloud", "Pages are straight and legible", "Figures have a text description"],
        "pitfalls": ["OCR cannot read handwriting reliably; type it or ask for an alternative format.", "Accessible-format rights for reading materials are set out in your local law; ask your school or library if unsure."],
    },
]
