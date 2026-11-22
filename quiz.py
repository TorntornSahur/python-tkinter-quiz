# quiz.py
# Networking Basics Quiz using Python Tkinter

import tkinter as tk
from tkinter import messagebox
import random
import os

# QUIZ DATA (list of dictionaries)
QUESTIONS = [
    {
        "question": "Which device forwards packets between different networks?",
        "choices": ["A. Hub", "B. Switch", "C. Router", "D. Repeater"],
        "answer": "C"
    },
    {
        "question": "What does DHCP do on a network?",
        "choices": ["A. Translates domain names", "B. Assigns IP addresses automatically",
                    "C. Encrypts traffic", "D. Filters packets"],
        "answer": "B"
    },
    {
        "question": "Which port number is used by HTTPS by default?",
        "choices": ["A. 80", "B. 21", "C. 25", "D. 443"],
        "answer": "D"
    },
    {
        "question": "How many bits long is an IPv4 address?",
        "choices": ["A. 32", "B. 64", "C. 128", "D. 48"],
        "answer": "A"
    },
    {
        "question": "Which topology connects each device to two neighbors, forming a closed loop?",
        "choices": ["A. Star", "B. Bus", "C. Ring", "D. Mesh"],
        "answer": "C"
    },
    {
        "question": "Which protocol translates domain names into IP addresses?",
        "choices": ["A. FTP", "B. DNS", "C. SMTP", "D. ARP"],
        "answer": "B"
    },
    {
        "question": "Which command tests whether a host can be reached using ICMP echo requests?",
        "choices": ["A. ping", "B. netstat", "C. route", "D. ipconfig"],
        "answer": "A"
    },
    {
        "question": "Which layer of the OSI model is responsible for routing?",
        "choices": ["A. Data Link", "B. Transport", "C. Session", "D. Network"],
        "answer": "D"
    },
    {
        "question": "How many bits long is a MAC address?",
        "choices": ["A. 32", "B. 48", "C. 64", "D. 128"],
        "answer": "B"
    },
    {
        "question": "Which cable type transmits data using pulses of light?",
        "choices": ["A. UTP", "B. Coaxial", "C. Fiber optic", "D. Serial"],
        "answer": "C"
    }
]

# APPLICATION SETTINGS
TIME_LIMIT = 10  # seconds per question
HIGH_SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_score.txt"
)

# Dark "control panel" theme
BG_COLOR = "#0B1220"        # window background
PANEL_COLOR = "#16213A"     # cards and sidebar
CHOICE_COLOR = "#1E2B4A"    # answer buttons
PRIMARY_COLOR = "#22D3EE"   # cyan accent
TEXT_COLOR = "#E6EDF7"
MUTED_COLOR = "#8A99B5"
CORRECT_COLOR = "#34D399"
WRONG_COLOR = "#F87171"
WARN_COLOR = "#FBBF24"
FONT = "Consolas"           # monospaced "terminal" look
TITLE_FONT = "Impact"

root = tk.Tk()
root.title("NetQuiz")
root.geometry("940x600")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# QUIZ STATE VARIABLES
quiz_questions = []   # shuffled copy of the questions
current_question = 0  # index of the current question
score = 0
time_left = TIME_LIMIT
wrong_answers = []    # stores details of incorrect answers
timer_job = None      # id of the scheduled timer (needed to cancel it)
answered = False      # becomes True after a question is submitted

selected_answer = tk.StringVar()

# Widgets that are updated while the quiz is running
timer_canvas = None
feedback_label = None
submit_button = None
next_button = None
choice_buttons = []

main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill="both", expand=True)


# HIGH SCORE FUNCTIONS (file handling)
def get_high_score():
    """Read the saved high score. Return 0 if there is no valid file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except ValueError:
            return 0
    return 0


def save_high_score(new_score):
    """Save the score only if it beats the old high score."""
    if new_score > get_high_score():
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(new_score))
        return True
    return False


# HELPER FUNCTIONS
def clear_screen():
    """Remove every widget from the main frame."""
    for widget in main_frame.winfo_children():
        widget.destroy()


def get_choice_text(question, letter):
    """Return the full choice text (for example 'B. Switch') from a letter."""
    for choice in question["choices"]:
        if choice.startswith(letter + "."):
            return choice
    return "No answer"


def make_button(parent, text, command, color=PRIMARY_COLOR, width=16, state="normal"):
    """Flat button used across all screens."""
    return tk.Button(parent, text=text, command=command, state=state,
                     font=(FONT, 12, "bold"), bg=color, fg=BG_COLOR,
                     activebackground=TEXT_COLOR, activeforeground=BG_COLOR,
                     disabledforeground=MUTED_COLOR, relief="flat", bd=0, highlightthickness=0,
                     width=width, pady=8, cursor="hand2")


def draw_timer():
    """Redraw the circular countdown in the sidebar."""
    timer_canvas.delete("all")
    color = WRONG_COLOR if time_left <= 5 else PRIMARY_COLOR
    timer_canvas.create_oval(10, 10, 150, 150, outline=CHOICE_COLOR, width=10)
    if time_left > 0:
        timer_canvas.create_arc(10, 10, 150, 150, start=90,
                                extent=min(359.9, 360 * time_left / TIME_LIMIT),
                                style="arc", outline=color, width=10)
    timer_canvas.create_text(80, 70, text=str(time_left),
                             font=(FONT, 34, "bold"), fill=color)
    timer_canvas.create_text(80, 106, text="seconds left",
                             font=(FONT, 9), fill=MUTED_COLOR)


def highlight_correct(question):
    """Turn the correct choice green after the question is closed."""
    for button in choice_buttons:
        if button["value"] == question["answer"]:
            button.config(bg=CORRECT_COLOR, selectcolor=CORRECT_COLOR,
                          disabledforeground=BG_COLOR)


# SCREENS
def show_start_screen():
    clear_screen()
    # Top banner
    banner = tk.Frame(main_frame, bg=PANEL_COLOR)
    banner.pack(fill="x")
    tk.Label(banner, text="> NETQUIZ_", font=(TITLE_FONT, 40),
             bg=PANEL_COLOR, fg=PRIMARY_COLOR).pack(pady=(35, 0))

    # Three info tiles
    tiles = tk.Frame(main_frame, bg=BG_COLOR)
    tiles.pack(pady=45)
    info = [(str(len(QUESTIONS)), "QUESTIONS"),
            (f"{TIME_LIMIT}s", "PER QUESTION"),
            (f"{get_high_score()}/{len(QUESTIONS)}", "HIGH SCORE")]
    for value, caption in info:
        tile = tk.Frame(tiles, bg=PANEL_COLOR, width=200, height=120)
        tile.pack(side="left", padx=15)
        tile.pack_propagate(False)
        tk.Label(tile, text=value, font=(FONT, 28, "bold"),
                 bg=PANEL_COLOR, fg=TEXT_COLOR).pack(pady=(25, 0))
        tk.Label(tile, text=caption, font=(FONT, 10),
                 bg=PANEL_COLOR, fg=MUTED_COLOR).pack()

    make_button(main_frame, "[ START QUIZ ]", start_quiz, width=22).pack()


def start_quiz():
    """Reset everything and shuffle the questions."""
    global quiz_questions, current_question, score, wrong_answers
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()


def show_question():
    global time_left, answered, timer_canvas, feedback_label
    global submit_button, next_button, choice_buttons
    clear_screen()
    answered = False
    selected_answer.set("")
    time_left = TIME_LIMIT
    question = quiz_questions[current_question]
    total = len(quiz_questions)

    # LEFT SIDEBAR: progress, timer, score
    sidebar = tk.Frame(main_frame, bg=PANEL_COLOR, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="PROGRESS", font=(FONT, 10), bg=PANEL_COLOR,
             fg=MUTED_COLOR).pack(pady=(30, 0))
    tk.Label(sidebar, text=f"Question {current_question + 1} of {total}",
             font=(FONT, 14, "bold"), bg=PANEL_COLOR,
             fg=TEXT_COLOR).pack(pady=(2, 8))

    # Segmented progress strip: one block per question
    strip = tk.Frame(sidebar, bg=PANEL_COLOR)
    strip.pack()
    for i in range(total):
        if i < current_question:
            block_color = PRIMARY_COLOR
        elif i == current_question:
            block_color = WARN_COLOR
        else:
            block_color = CHOICE_COLOR
        tk.Frame(strip, bg=block_color, width=16, height=8).pack(side="left", padx=1)

    timer_canvas = tk.Canvas(sidebar, width=160, height=160, bg=PANEL_COLOR,
                             highlightthickness=0)
    timer_canvas.pack(pady=30)

    tk.Label(sidebar, text="SCORE", font=(FONT, 10), bg=PANEL_COLOR,
             fg=MUTED_COLOR).pack()
    tk.Label(sidebar, text=f"{score} / {total}", font=(FONT, 22, "bold"),
             bg=PANEL_COLOR, fg=CORRECT_COLOR).pack()

    # Restart button available during the quiz too
    make_button(sidebar, "RESTART", confirm_restart, color=WRONG_COLOR,
                width=14).pack(side="bottom", pady=25)

    # RIGHT SIDE: question card, choices, feedback, buttons
    content = tk.Frame(main_frame, bg=BG_COLOR)
    content.pack(side="left", fill="both", expand=True, padx=30, pady=25)

    card = tk.Frame(content, bg=PANEL_COLOR)
    card.pack(fill="x", pady=(0, 14))
    tk.Label(card, text=question["question"], font=(FONT, 15, "bold"),
             wraplength=580, justify="left", bg=PANEL_COLOR,
             fg=TEXT_COLOR).pack(padx=20, pady=22, anchor="w")

    # Answer choices styled as buttons (the value of each is its letter)
    choice_buttons = []
    for choice in question["choices"]:
        letter = choice[0]
        button = tk.Radiobutton(content, text=choice, variable=selected_answer,
                                value=letter, indicatoron=0, anchor="w",
                                font=(FONT, 12), bg=CHOICE_COLOR, fg=TEXT_COLOR,
                                selectcolor="#2B4A7A",
                                activebackground="#2B4A7A",
                                activeforeground=TEXT_COLOR,
                                disabledforeground=MUTED_COLOR,
                                relief="flat", bd=0, padx=15, pady=9,
                                highlightthickness=0, cursor="hand2")
        button.pack(fill="x", pady=4)
        choice_buttons.append(button)

    feedback_label = tk.Label(content, text="", font=(FONT, 12, "bold"),
                              bg=BG_COLOR, wraplength=580, justify="left")
    feedback_label.pack(pady=12, anchor="w")

    button_frame = tk.Frame(content, bg=BG_COLOR)
    button_frame.pack(anchor="w")

    submit_button = make_button(button_frame, "SUBMIT", submit_answer)
    submit_button.pack(side="left", padx=(0, 12))

    last_question = current_question == total - 1
    next_button = make_button(button_frame,
                              "SEE RESULTS" if last_question else "NEXT >>",
                              next_question, color=WARN_COLOR, state="disabled")
    next_button.pack(side="left")

    update_timer()


# TIMER
def update_timer():
    """Runs once per second until the question is answered or time is up."""
    global time_left, timer_job
    if answered:
        return
    draw_timer()
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    """Cancel the scheduled timer so it stops counting down."""
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


# ANSWER CHECKING
def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")


def submit_answer():
    global score, answered
    if answered:  # blocks multiple submissions
        return
    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")
    question = quiz_questions[current_question]
    if choice == question["answer"]:
        score += 1
        feedback_label.config(text="[OK] Correct!", fg=CORRECT_COLOR)
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": get_choice_text(question, choice),
            "correct_answer": get_choice_text(question, question["answer"])
        })
        feedback_label.config(
            text="[X] Wrong! Correct answer: "
                 + get_choice_text(question, question["answer"]),
            fg=WRONG_COLOR)
    highlight_correct(question)
    next_button.config(state="normal")


def time_up():
    """Called when the timer reaches zero."""
    global answered
    answered = True
    lock_choices()
    submit_button.config(state="disabled")
    question = quiz_questions[current_question]
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": get_choice_text(question, question["answer"])
    })
    feedback_label.config(
        text="[!] Time is up! Correct answer: "
             + get_choice_text(question, question["answer"]),
        fg=WRONG_COLOR)
    highlight_correct(question)
    next_button.config(state="normal")


def next_question():
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()


# RESULTS, REVIEW, RESTART
def show_results():
    clear_screen()
    total = len(quiz_questions)
    percentage = (score / total) * 100
    new_record = save_high_score(score)

    if percentage >= 90:
        message = "Excellent work!"
    elif percentage >= 70:
        message = "Good job!"
    elif percentage >= 50:
        message = "Not bad. Keep practicing!"
    else:
        message = "Review the topic and try again."

    # LEFT PANEL: score summary and buttons
    summary = tk.Frame(main_frame, bg=PANEL_COLOR, width=330)
    summary.pack(side="left", fill="y")
    summary.pack_propagate(False)

    tk.Label(summary, text="QUIZ COMPLETE", font=(FONT, 12, "bold"),
             bg=PANEL_COLOR, fg=MUTED_COLOR).pack(pady=(35, 5))
    tk.Label(summary, text=f"{score}/{total}", font=(TITLE_FONT, 60),
             bg=PANEL_COLOR, fg=PRIMARY_COLOR).pack()
    tk.Label(summary, text=f"{percentage:.0f}%", font=(FONT, 22, "bold"),
             bg=PANEL_COLOR, fg=TEXT_COLOR).pack()
    tk.Label(summary, text=message, font=(FONT, 12), wraplength=280,
             bg=PANEL_COLOR, fg=WARN_COLOR).pack(pady=12)
    record_text = "** NEW HIGH SCORE **" if new_record else f"High Score: {get_high_score()} / {total}"
    tk.Label(summary, text=record_text, font=(FONT, 12, "bold"),
             bg=PANEL_COLOR, fg=CORRECT_COLOR).pack(pady=5)

    make_button(summary, "RESTART", restart_quiz, width=20).pack(pady=(30, 8))
    make_button(summary, "EXIT", on_close, color=WRONG_COLOR, width=20).pack()

    # RIGHT PANEL: answer review
    right = tk.Frame(main_frame, bg=BG_COLOR)
    right.pack(side="left", fill="both", expand=True, padx=25, pady=25)
    tk.Label(right, text="ANSWER REVIEW (incorrect answers)",
             font=(FONT, 12, "bold"), bg=BG_COLOR,
             fg=TEXT_COLOR).pack(anchor="w", pady=(0, 8))

    review_frame = tk.Frame(right, bg=BG_COLOR)
    review_frame.pack(fill="both", expand=True)
    scrollbar = tk.Scrollbar(review_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(review_frame, wrap="word", font=(FONT, 11),
                         bg=PANEL_COLOR, fg=TEXT_COLOR, relief="flat",
                         padx=15, pady=12, highlightthickness=0,
                         yscrollcommand=scrollbar.set)
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)
    review_box.tag_config("q", foreground=TEXT_COLOR, font=(FONT, 11, "bold"))
    review_box.tag_config("bad", foreground=WRONG_COLOR)
    review_box.tag_config("good", foreground=CORRECT_COLOR)

    if not wrong_answers:
        review_box.insert("end", "Perfect! You answered every question correctly.", "good")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n", "q")
            review_box.insert("end", f"   Your answer: {item['your_answer']}\n", "bad")
            review_box.insert("end", f"   Correct answer: {item['correct_answer']}\n\n", "good")
    review_box.config(state="disabled")


def restart_quiz():
    stop_timer()  # cancel any running countdown before resetting
    start_quiz()  # reshuffles questions and resets score


def confirm_restart():
    """Ask before restarting in the middle of a quiz."""
    if messagebox.askyesno("Restart", "Restart the quiz? Your current progress will be lost."):
        restart_quiz()


def on_close():
    stop_timer()
    root.destroy()


# START THE PROGRAM
root.protocol("WM_DELETE_WINDOW", on_close)
show_start_screen()
root.mainloop()
