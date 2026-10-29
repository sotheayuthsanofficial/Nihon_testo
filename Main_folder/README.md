# 🌸 Japanese Quest — Hiragana & Katakana Quiz

**Japanese Quest** is an interactive Japanese alphabet learning application built with Python and Streamlit. It helps beginners practice recognizing Hiragana and Katakana characters and learning their Romaji pronunciations through an image-based multiple-choice quiz.

## ✨ Features

- **Two Learning Sections:** Choose between Hiragana (ひらがな) and Katakana (カタカナ).
- **PDF-Based Character Cards:** Display Japanese characters using images rendered from PDF files.
- **Four Multiple-Choice Answers:** Select the correct pronunciation from four options.
- **Randomized Questions:** Shuffle questions and answer choices when starting a new game.
- **Instant Feedback:** See whether an answer is correct and learn the correct pronunciation.
- **Score Tracking:** Earn 1 point for a correct answer or lose 1 point for an incorrect answer.
- **Streak Tracking:** Keep track of consecutive correct answers.
- **Progress Bar:** Monitor progress through the quiz.
- **Question Navigation:** Move between questions using Previous and Next buttons.
- **Results Dashboard:** Review your final score, accuracy, correct answers, and incorrect answers.
- **Replay and Navigation:** Play again in the same section or return to the main menu.
- **Custom User Interface:** Enjoy a soft green theme, rounded character cards, styled buttons, and a circular accuracy indicator.
- **PDF Validation:** Check for missing files, unconfirmed answers, unreadable PDFs, and mismatches between filenames and answer mappings.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Quiz logic, scoring, and application behavior |
| Streamlit | Interactive web application interface |
| PyMuPDF (`fitz`) | Read PDF files and render character images |
| HTML and CSS | Customize cards, buttons, colors, and layout |
| Base64 | Embed navigation button images in CSS |

## 📂 Project Structure

The following is a suggested organization for the project:

```text
Japanese-Quest/
├── app.py
├── requirements.txt
├── README.md
├── Hiragana/
│   ├── a.pdf
│   ├── i.pdf
│   ├── u.pdf
│   └── ...
├── Katakana/
│   ├── a.pdf
│   ├── i.pdf
│   ├── u.pdf
│   └── ...
├── arrow_previous.jpg
└── arrow_next.jpg
```

The filenames and folder names above are examples. Your application currently uses configurable folder paths, so you can keep your PDF collections elsewhere on your computer.

The navigation arrow images are optional. If the configured image files cannot be found, the navigation buttons can still display their text labels.

### 2. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Japanese-Quest
```

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the PDF folders

Open `app.py` and locate these variables:

```python
# You need to use path here
hiragana_folder = "Hiragana path"
katakana_folder = "Katakana path"
```

Replace the placeholder values with the actual paths to your PDF folders.

For example, on Windows:

```python
hiragana_folder = r"C:\Japanese-Quest\Hiragana"
katakana_folder = r"C:\Japanese-Quest\Katakana"
```

**Important:** You need to use path here. Make sure the folders exist and contain the correct PDF files.

### 5. Confirm the answer mappings

The application uses separate dictionaries named `hiragana_answers` and `katakana_answers`.

Each dictionary connects a PDF filename, without the `.pdf` extension, to its correct Romaji pronunciation.

For example:

```python
hiragana_answers = {
    "a": "a",
    "i": "i",
    "u": "u",
    "e": "e",
    "o": "o"
}
```

Make sure every filename matches its corresponding PDF and every pronunciation is correct.

For example, `"o(1)"` and `"o (1)"` are different filenames. Check the actual filename in your folder before changing the answer mapping.

### 6. Run the application

```bash
streamlit run app.py
```

## 🎮 How to Play

1. Open Japanese Quest.
2. Choose **Hiragana Quest** or **Katakana Quest** from the main menu.
3. Study the character displayed on the screen.
4. Select one of the four pronunciation choices.
5. Review the feedback and the correct answer.
6. Use Previous or Next to navigate between questions.
7. Select Home to return to the section-selection page.
8. Finish the quiz to view your results.
9. Choose Play Again to start a new game in the same section.

## 🎯 Project Objectives

- Make Japanese alphabet practice interactive and engaging.
- Help beginners recognize Hiragana and Katakana characters.
- Practice Japanese character-to-Romaji recognition.
- Provide immediate feedback during learning.
- Encourage repeated practice through randomized quizzes.
- Apply Python programming and Streamlit skills to a practical educational project.

## 👨‍💻 Author

Developed as a personal learning project to explore Python, Streamlit, PDF processing, and interactive educational application development.

## 📄 License

Choose a suitable license before publishing the project. Make sure you have permission to share any PDF learning materials included in the repository. If the PDFs cannot be redistributed, provide instructions for users to supply their own files instead.