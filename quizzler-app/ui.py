from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score = 0
        self.score = Label(text=f"Score: {self.score}", bg=THEME_COLOR)
        self.score.grid(row=0, column=1)

        # Question Text
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question = self.canvas.create_text(150, 125, width=200, text=f"{self.quiz.next_question()}", font=("Arial", 15, "italic"))
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        # Buttons
        true_img = PhotoImage(file="images/true.png")
        self.true_button = Button(image=true_img, highlightthickness=0, command=self.clicked_true)
        self.true_button.grid(row=2, column=0)
        false_img = PhotoImage(file="images/false.png")
        self.false_button = Button(image=false_img, highlightthickness=0, command=self.clicked_false)
        self.false_button.grid(row=2, column=1)

        self.window.mainloop()

    def show_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.canvas.itemconfig(self.question, text=f"{self.quiz.next_question()}")
        else:
            self.canvas.itemconfig(self.question, text=f"You've completed the quiz\nYour final score was: {self.quiz.score}/10")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
        self.score.config(text=f"Score: {self.quiz.score}")

    def clicked_true(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def clicked_false(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, answer):
        if answer:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000, self.show_question)
