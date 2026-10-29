import os
import random
import fitz
import streamlit as st
import base64

# You need to use path here
hiragana_folder = "Hiragana path"
katakana_folder = "Katakana path"

previous_image = "arrow_previous.jpg"
next_image = "arrow_next.jpg"
# File name (without .pdf) -> correct answer.
# None means "not confirmed yet". Replace None with the real answer.
# Add or delete lines so this list matches your files exactly.
katakana_answers = {
    "a": "a", "i": "i", "u": "u", "e": "e", "o": "o",
    "ka": "ka", "ki": "ki", "ku": "ku", "ke": "ke", "ko": "ko",
    "sa": "sa", "shi": "shi", "su": "su", "se": "se", "so": "so",
    "ta": "ta", "chi": "chi", "tsu": "tsu", "te": "te", "to": "to",
    "na": "na", "ni": "ni", "nu": "nu", "ne": "ne", "no": "no",
    "ha": "ha", "hi": "hi", "fu": "fu", "he": "he", "ho": "ho",
    "ma": "ma", "mi": "mi", "mu": "mu", "me": "me", "mo": "mo",
    "ya": "ya", "yu": "yu", "yo": "yo",
    "ra": "ra", "ri": "ri", "ru": "ru", "re": "re", "ro": "ro",
    "wa": "wa", "n": "n",
    "o(1)": "wo"
}
hiragana_answers = {
    "a": "a", "i": "i", "u": "u", "e": "e", "o": "o",
    "ka": "ka", "ki": "ki", "ku": "ku", "ke": "ke", "ko": "ko",
    "sa": "sa", "shi": "shi", "su": "su", "se": "se", "so": "so",
    "ta": "ta", "chi": "chi", "tsu": "tsu", "te": "te", "to": "to",
    "na": "na", "ni": "ni", "nu": "nu", "ne": "ne", "no": "no",
    "ha": "ha", "hi": "hi", "fu": "fu", "he": "he", "ho": "ho",
    "ma": "ma", "mi": "mi", "mu": "mu", "me": "me", "mo": "mo",
    "ya": "ya", "yu": "yu", "yo": "yo",
    "ra": "ra", "ri": "ri", "ru": "ru", "re": "re", "ro": "ro",
    "wa": "wa", "o (1)": "wo", "n": "n",
}

# Each section keeps its own folder and answers, so they never mix
sections = {
    "hiragana": {
        "name": "Hiragana",
        "script": "ひらがな",
        "text": "Soft, round characters used in everyday Japanese words. A great place to begin.",
        "folder": hiragana_folder,
        "answers": hiragana_answers,
    },
    "katakana": {
        "name": "Katakana",
        "script": "カタカナ",
        "text": "Sharp, angular characters used for foreign words and names.",
        "folder": katakana_folder,
        "answers": katakana_answers,
    },
}


st.set_page_config(page_title="Japanese Learning tool", layout="centered")

st.markdown("""
<style>

/* ==================================================
   1. APPLICATION BACKGROUND
   ================================================== */

/* Set a soft gray-green background for the entire application. */
.stApp {
    background-color: #F3F5F4;
}


/* ==================================================
   2. HEADINGS AND TEXT
   ================================================== */

/* Style the main headings and center them on the page. */
h1, h2, h3 {
    color: #3F6B52;
    text-align: center;
}

/* Make normal Markdown paragraph text dark and readable. */
.stMarkdown p {
    color: #26352C;
}

/* Style subtitles displayed using the custom sub class. */
.sub {
    text-align: center;
    color: #5F6F66;
    font-size: 18px;
}

/* Style large Japanese characters when using the big class. */
.big {
    font-size: 64px;
    font-weight: bold;
    text-align: center;
    color: #3F6B52;
}

/* Make the question and result text readable. */
.stMarkdown p {
    color: #26352C !important;
}

/* Make the question subtitle larger and easier to read. */
.sub {
    text-align: center;
    color: #26352C !important;
    font-size: 20px;
    font-weight: 500;
}

/* Make the result statistics labels readable. */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #5F6F66 !important;
    font-size: 16px;
}

/* Make the result statistics numbers readable. */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #3F6B52 !important;
    font-size: 32px;
}

/* Make feedback messages readable on their colored backgrounds. */
[data-testid="stAlert"],
[data-testid="stAlert"] p {
    color: #26352C !important;
}

/* Keep the question header text dark green. */
.top,
.top p,
.top div {
    color: #3F6B52 !important;
}

/* ==================================================
   3. QUESTION HEADER
   ================================================== */

/* Style the box that displays the question number and score. */
.top {
    background: #E8F5EC;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    font-weight: bold;
    color: #3F6B52;
}

/* Keep text inside the question header dark green. */
.top p,
.top div,
.top span {
    color: #3F6B52;
}


/* ==================================================
   4. IMAGE CARD
   ================================================== */

/* Make the image row full width and center the card in it, on every screen. */
div[data-testid="stElementContainer"]:has([data-testid="stImage"]),
div.element-container:has([data-testid="stImage"]) {
    display: flex;
    justify-content: center;
    width: 100% !important;
}

/* The white card hugs the letter. */
[data-testid="stImage"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: fit-content;
    background: #FFFFFF;
    border-radius: 20px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    box-sizing: border-box;
}

/* Keep images within the available container width. */
[data-testid="stImage"] img {
    max-width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 8px;
}


/* ==================================================
   5. ANSWER BUTTONS
   ================================================== */

/* Give all Streamlit buttons a consistent appearance. */
div.stButton > button {
    width: 100%;
    min-height: 65px;
    font-size: 20px;
    font-weight: 500;
    border-radius: 16px;
    border: 2px solid #D9E0DC;
    background: #FFFFFF;
    color: #26352C;
    transition: background-color 0.2s ease,
                border-color 0.2s ease;
}

/* Highlight buttons when the mouse moves over them. */
div.stButton > button:hover {
    border-color: #A8D5BA;
    background: #E8F5EC;
    color: #26352C;
}

/* Keep disabled buttons readable after an answer is selected. */
div.stButton > button:disabled {
    opacity: 1;
    color: #26352C;
}

/* Highlight primary buttons using the green theme. */
div.stButton > button[kind="primary"],
div.stButton > button[data-testid="stBaseButton-primary"] {
    background: #A8D5BA;
    border-color: #3F6B52;
    color: #26352C;
}

/* Add a darker border when a primary button is hovered over. */
div.stButton > button[kind="primary"]:hover,
div.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: #93C9A7;
    border-color: #315740;
}


/* ==================================================
   6. PROGRESS BAR
   ================================================== */

/* Give the progress bar rounded corners. */
.stProgress > div > div {
    border-radius: 10px;
    overflow: hidden;
}

/* Use light green for the completed part of the progress bar. */
.stProgress > div > div > div {
    background-color: #A8D5BA;
    border-radius: 10px;
}


/* ==================================================
   7. RESULTS PAGE: SCORE AND STATISTICS
   ================================================== */

/* Make metric labels readable on the light background. */
[data-testid="stMetricLabel"] {
    color: #5F6F66;
}

/* Make metric values dark green and easy to read. */
[data-testid="stMetricValue"] {
    color: #3F6B52;
}

/* Improve the appearance of results-page headings. */
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3 {
    color: #3F6B52;
}

/* Make text inside Streamlit informational messages readable. */
[data-testid="stAlert"] {
    color: #26352C;
}

/* Keep paragraphs inside informational messages dark. */
[data-testid="stAlert"] p {
    color: #26352C;
}


/* ==================================================
   8. PROGRESS RING: OUTER CIRCLE
   ================================================== */

/* Create the outer circle used to display quiz accuracy.
   The background can be set dynamically using a conic gradient. */
.ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
}


/* ==================================================
   9. PROGRESS RING: INNER CIRCLE
   ================================================== */

/* Create a white inner circle to form the ring shape.
   Center the percentage text inside the circle. */
.ring-inner {
    width: 105px;
    height: 105px;
    border-radius: 50%;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: bold;
    color: #3F6B52;
}


/* ==================================================
   10. FEEDBACK AND MESSAGE TEXT
   ================================================== */

/* Set readable text colors for custom feedback messages. */
.feedback {
    color: #26352C;
    font-size: 16px;
    line-height: 1.6;
}

/* Style the feedback message container. */
.feedback-box {
    background: #E8F5EC;
    border-radius: 12px;
    padding: 16px;
    color: #26352C;
}

/* Make text inside custom feedback boxes readable. */
.feedback-box p,
.feedback-box span,
.feedback-box div {
    color: #26352C;
}


/* ==================================================
   11. RESPONSIVE LAYOUT
   ================================================== */

/* Adjust text sizes and card spacing for smaller screens. */
@media (max-width: 640px) {

    /* Reduce the size of large Japanese characters on mobile. */
    .big {
        font-size: 48px;
    }

    /* Make answer buttons slightly smaller on mobile. */
    div.stButton > button {
        min-height: 55px;
        font-size: 18px;
        border-radius: 12px;
    }

    /* Reduce image card padding on mobile. */
    [data-testid="stImage"] {
        padding: 10px;
        border-radius: 16px;
    }

    /* Reduce progress ring size on mobile. */
    .ring {
        width: 120px;
        height: 120px;
    }

    /* Adjust the inner circle to match the smaller ring. */
    .ring-inner {
        width: 90px;
        height: 90px;
        font-size: 24px;
    }
}

/* ==================================================
   12. SECTION CARDS (main menu)
   ================================================== */

.card {
    background: #E8F5EC;
    border: 2px solid #D9E0DC;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Highlight the card when the mouse moves over it. */
.card:hover {
    border-color: #A8D5BA;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
}

.card-script { font-size: 44px; font-weight: bold; color: #3F6B52; }
.card-title { font-size: 22px; font-weight: bold; color: #26352C; }
.card-text { font-size: 16px; color: #26352C; margin-top: 8px; }

/* ==================================================
   13. SLIDER (main page)
   ================================================== */

/* Dark green slider handle and readable slider text. */
div[data-baseweb="slider"] div[role="slider"] {
    background-color: #3F6B52 !important;
    border-color: #3F6B52 !important;
}

[data-testid="stSlider"] label p,
[data-testid="stSlider"] p {
    color: #26352C !important;
    font-size: 18px;
}
/* ==================================================
   14. SLIDING CARDS (page 1)
   ================================================== */

/* A row of cards you can slide sideways. Each card snaps into place. */
.slider {
    display: flex;
    gap: 16px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    padding: 8px 4px 16px 4px;
    scrollbar-width: thin;
    scrollbar-color: #A8D5BA #E8F5EC;
}

/* Each card takes 80% of the width, so the next card peeks in from the side. */
a.slide, .stMarkdown a.slide, .slide {
    flex: 0 0 80%;
    scroll-snap-align: center;
    display: block;
    text-decoration: none !important;
}

.slide .card {
    height: 100%;
    box-sizing: border-box;
    margin-bottom: 0;
    cursor: pointer;
}

/* Small press effect when a card is tapped. */
.slide:active .card { transform: scale(0.98); }

/* A card that cannot start yet. */
.slide.off .card { opacity: 0.6; cursor: not-allowed; }

.card-tap { margin-top: 12px; font-weight: bold; color: #3F6B52; }


/* ==================================================
   15. QUIZ BUTTON ROWS (page 2)
   ================================================== */

/* Keep the answer row and the navigation row side by side on phones too,
   instead of letting Streamlit stack the columns. */
.st-key-answers [data-testid="stHorizontalBlock"],
.st-key-nav [data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
}

.st-key-answers [data-testid="stColumn"],
.st-key-answers [data-testid="column"],
.st-key-nav [data-testid="stColumn"],
.st-key-nav [data-testid="column"] {
    min-width: 0 !important;
    width: auto !important;
    flex: 1 1 0 !important;
}

/* Navigation row: a tiny gap makes each button about 2/5 of an answer card. */
.st-key-nav [data-testid="stHorizontalBlock"] {
    gap: 2px !important;
}

/* Navigation buttons are smaller than the answer buttons. */
.st-key-nav div.stButton > button {
    min-height: 44px;
    font-size: 14px;
    padding: 4px 2px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

def make_pool(answers):
    # All different confirmed answers of one section (used to make wrong choices)
    return sorted(set([x for x in answers.values() if x is not None]))

def check_files(folder, answers):
    # Return a list of error messages. Empty list = everything is OK
    errors = []
    if not os.path.isdir(folder):
        errors.append("Folder not found: " + folder + ". Change 'folder' at the top of the code.")
        return errors

    stems = []
    for file_name in os.listdir(folder):
        if file_name.endswith(".pdf"):
            stems.append(file_name[:-4])

    # PDF files that are not in the answers list
    for stem in stems:
        if stem not in answers:
            errors.append(stem + ".pdf is in your folder but not in the 'answers' list. Add it.")

    # Items in the answers list
    for stem in answers:
        if answers[stem] is None:
            errors.append(stem + ".pdf: answer is not confirmed. Replace None with the real answer.")
        if stem not in stems:
            errors.append(stem + ".pdf is in the 'answers' list but not in your folder.")
        else:
            try:
                doc = fitz.open(os.path.join(folder, stem + ".pdf"))
                if doc.page_count == 0:
                    errors.append(stem + ".pdf has no pages.")
            except Exception:
                errors.append(stem + ".pdf cannot be opened. The file may be broken.")

    if len(make_pool(answers)) < 4:
        errors.append("You need at least 4 different answers to make 4 choices.")
    return errors


@st.cache_data
def get_image(folder_path, stem):
    # Turn page 1 of the PDF into a PNG image (cached, so it is only done once)
    doc = fitz.open(os.path.join(folder_path, stem + ".pdf"))
    page = doc[0]

    # Card shape = width / height. A bigger number makes the card wider and shorter.
    # Adjustable. About 0.61 or lower keeps the original shape of the PDF.
    card_ratio = 0.73

    # Keep the full width and cut the same amount from the top and bottom
    rect = page.rect
    new_height = rect.width / card_ratio
    cut = (rect.height - new_height) / 2
    if cut > 0:
        clip = fitz.Rect(rect.x0, rect.y0 + cut, rect.x1, rect.y1 - cut)
    else:
        clip = rect

    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip)
    return pix.tobytes("png")

@st.cache_data
def arrow_css(image_path, button_key):
    # Make the picture the background of the button that has this key.
    # If the picture is not found, return nothing, so the button stays as text.
    if not os.path.isfile(image_path):
        return ""
    with open(image_path, "rb") as file:
        text = base64.b64encode(file.read()).decode("utf-8")

    selector = ".st-key-" + button_key + " div.stButton > button"
    css = (selector + " { background-image: url(data:image/jpeg;base64," + text + "); "
           + "background-size: contain; background-repeat: no-repeat; "
           + "background-position: center; background-color: #FFFFFF !important; } ")

    # Hide the word on the button, and make the button lighter when it is disabled
    css = css + selector + " p { color: transparent !important; } "
    css = css + selector + ":disabled { opacity: 0.35; } "
    return css

def start_game(section_key):
    # Start a fresh game for the chosen section
    answers = sections[section_key]["answers"]
    pool = make_pool(answers)

    # Random question order
    names = list(answers.keys())
    random.shuffle(names)

    # 4 choices for each question: 3 wrong + 1 correct, then shuffled.
    # Saved once here, so they do not change when Streamlit reruns.
    choices = {}
    for stem in names:
        correct = answers[stem]
        others = [x for x in pool if x != correct]
        options = random.sample(others, 3) + [correct]
        random.shuffle(options)
        choices[stem] = options

    st.session_state.section = section_key
    st.session_state.names = names
    st.session_state.choices = choices
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.streak = 0
    st.session_state.page = "quiz"
    st.session_state.given = {}


def go_menu():
    # Go back to the section page and delete the old game, so nothing carries over
    for key in ["names", "choices", "index", "score", "correct", "wrong",
                "streak", "given", "submitted", "selected"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.section = None
    st.session_state.page = "menu"


if "page" not in st.session_state:
    st.session_state.page = "menu"
if "section" not in st.session_state:
    st.session_state.section = None

# A tapped card opens the app with ?start=hiragana or ?start=katakana
if "start" in st.query_params:
    chosen = st.query_params["start"]
    st.query_params.clear()
    if chosen in sections:
        if len(check_files(sections[chosen]["folder"], sections[chosen]["answers"])) == 0:
            start_game(chosen)

# Safety: a quiz or result page needs a chosen section
if st.session_state.page not in {"menu", "quiz", "result"}:
    go_menu()
elif st.session_state.page != "menu" and st.session_state.section not in sections:
    go_menu()

# Page 1: slide the cards sideways like a phone, tap a card to start
if st.session_state.page == "menu":
    st.title("🌸 Japanese Quest")
    st.markdown('<p class="sub">Choose Your Path. Master Japanese.</p>',
                unsafe_allow_html=True)
    st.write("This app helps you practice Japanese characters and their sounds. "
             "You will see one character and choose the correct sound from 4 answers.")
    st.write("Correct answer: +1 point. Wrong answer: -1 point. Your score can go below zero.")

    # Build one card per section. A card is a link only if its files are OK.
    slides = ""
    problems = {}
    for key in ["hiragana", "katakana"]:
        section = sections[key]
        errors = check_files(section["folder"], section["answers"])
        if len(errors) == 0:
            hint = "Tap to start"
        else:
            hint = "Fix the problems below first"
            problems[key] = errors

        inside = ('<div class="card"><div class="card-script">' + section["script"]
                  + '</div><div class="card-title">' + section["name"] + ' Quest</div>'
                  + '<div class="card-text">' + section["text"] + '</div>'
                  + '<div class="card-tap">' + hint + '</div></div>')

        if len(errors) == 0:
            # Tapping the link opens the app with ?start=hiragana or ?start=katakana
            slides = slides + '<a class="slide" href="?start=' + key + '" target="_self">' + inside + '</a>'
        else:
            slides = slides + '<div class="slide off">' + inside + '</div>'

    st.markdown('<div class="slider">' + slides + '</div>', unsafe_allow_html=True)

    # Show the problems of a section that cannot start
    for key in problems:
        with st.expander(sections[key]["name"] + ": problems found (" + str(len(problems[key])) + ")"):
            for message in problems[key]:
                st.error(message)

# Page 2: quiz
elif st.session_state.page == "quiz":
    section_key = st.session_state.section
    if not isinstance(section_key, str) or section_key not in sections:
        go_menu()
        st.rerun()
    section = sections[section_key]
    answers = section["answers"]
    folder = section["folder"]
    names = st.session_state.names
    index = st.session_state.index
    total = len(names)
    name = names[index]
    correct = answers[name]
    options = st.session_state.choices[name]
        # A question is answered when it is saved in 'given'
    submitted = name in st.session_state.given
    selected = st.session_state.given.get(name)

    # Build the question header with the current question number and score.
    top = "QUESTION " + str(index + 1) + " / " + str(total)
    top = top + "<br>SCORE: " + str(st.session_state.score) + " POINTS"

    # Display the current winning streak when it reaches two answers.
    if st.session_state.streak >= 2:
        top = top + "<br>🔥 Streak: " + str(st.session_state.streak)

    # Display the header using the custom green style.
    st.markdown(
        '<div class="top">' + top + '</div>',
        unsafe_allow_html=True
    )

    # Calculate progress after accounting for the current question.
    progress = (index + 1) / total if total > 0 else 0

    # Display the progress bar.
    st.progress(progress)

# Display the question above the character card.
    st.markdown(
        '<p class="sub">Which sound does this character make?</p>',
        unsafe_allow_html=True
    )

    # The CSS centers the image card on every screen
    try:
        st.image(get_image(folder, name), width=240)
    except Exception:
        st.error("Cannot show " + name + ".pdf. Check the file.")
        st.stop()

    # Feedback appears only after the answer is submitted
    if submitted:
        if selected == correct:
            st.success("Sugoi! (すごい！) Great job! +1 point")
        else:
            st.warning("Not quite! Let's learn this one. -1 point. "
                       "The correct answer is " + correct.upper())

    # Keep the answer controls locked after a response so it is scored only once.
    with st.container(key="answers"):
        columns = st.columns(2)
        for i, option in enumerate(options):
            label = option.upper()
            key = "q" + str(index) + "_" + option
            if submitted:
                if option == correct:
                    columns[i % 2].button(
                        "✅ " + label, key=key, disabled=True, type="primary"
                    )
                elif option == selected:
                    columns[i % 2].button("❌ " + label, key=key, disabled=True)
                else:
                    columns[i % 2].button(label, key=key, disabled=True)
            elif columns[i % 2].button(label, key=key):
                st.session_state.given[name] = option
                if option == correct:
                    st.session_state.score += 1
                    st.session_state.correct += 1
                    st.session_state.streak += 1
                else:
                    st.session_state.score -= 1
                    st.session_state.wrong += 1
                    st.session_state.streak = 0
                st.rerun()

    # Keep navigation in one place to avoid duplicate Streamlit widget keys.
    with st.container(key="nav"):
        arrow_style = ""
        if index > 0:
            arrow_style += arrow_css(previous_image, "previous_question")
        if index + 1 < total:
            arrow_style += arrow_css(next_image, "next_question")
        if arrow_style:
            st.markdown("<style>" + arrow_style + "</style>", unsafe_allow_html=True)

        previous_column, _, home_column, _, next_column = st.columns(5)
        if index > 0 and previous_column.button(
            "Previous", key="previous_question"
        ):
            st.session_state.index -= 1
            st.rerun()

        if home_column.button("Home", key="home_quiz"):
            go_menu()
            st.rerun()

        next_label = "Finish" if index + 1 >= total else "Next"
        if next_column.button(
            next_label,
            key="next_question",
            type="primary",
            disabled=not submitted,
        ):
            if index + 1 >= total:
                st.session_state.page = "result"
            else:
                st.session_state.index += 1
            st.rerun()

# Page 3: result
elif st.session_state.page == "result":
    section_key = st.session_state.section
    if not isinstance(section_key, str) or section_key not in sections:
        go_menu()
        st.rerun()
    section = sections[section_key]
    total = len(st.session_state.names)
    correct_count = st.session_state.correct
    wrong_count = st.session_state.wrong

    # Safe when total is zero
    if total > 0:
        accuracy = correct_count / total * 100
    else:
        accuracy = 0

    st.title("🎉 " + section["name"] + " Results")
    st.markdown('<div class="big">' + str(st.session_state.score) + '</div>',
                unsafe_allow_html=True)
    st.markdown('<p class="sub">final score</p>', unsafe_allow_html=True)

    # Progress ring: green part = accuracy
    ring = ('<div class="ring" style="background: conic-gradient(#A8D5BA '
            + str(accuracy * 3.6) + 'deg, #D9E0DC 0deg);">'
            + '<div class="ring-inner">' + str(round(accuracy)) + '%</div></div>')
    st.markdown(ring, unsafe_allow_html=True)
    # Add space above the statistics section.
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Create three equal-width columns for the results statistics.
    col1, col2, col3 = st.columns(3)

    # Display the total number of questions.
    with col1:
        st.metric("Questions", total)

    # Display the number of correct answers.
    with col2:
        st.metric("Correct", correct_count)

    # Display the number of wrong answers.
    with col3:
        st.metric("Wrong", wrong_count)

    # Add space before the feedback message.
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Display feedback according to the user's accuracy.
    if accuracy >= 80:
        st.success("Amazing work! Keep exploring Japanese!")
    elif accuracy >= 50:
        st.info("Nice effort! Every question helps you improve.")
    else:
        st.info("Good start! Practice again and discover more characters.")
    # Play again stays in the same section
    if st.button("Play Again", type="primary"):
        start_game(section_key)
        st.rerun()

    if st.button("Back to Sections", key="menu_result"):
        go_menu()
        st.rerun()