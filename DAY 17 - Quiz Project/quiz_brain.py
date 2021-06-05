class QuizBrain:

    def __init__(self, bank):
        self.question_number = 0
        self.questions_list = bank
        self.score = 0

    def next_question(self):
        """Retrieves current question number from question list
        and prompts user for answer."""
        current_question = self.questions_list[self.question_number]
        self.question_number += 1

        user_answer = input(f"Q.{self.question_number}: {current_question.text}. (True/False)?: ")
        self.check_answer(user_answer, current_question.answer)

    def still_has_questions(self):
        """Returns true or false depending on number of questions in the list."""
        return self.question_number < len(self.questions_list)

    def check_answer(self, user_answer, question_answer):
        """Checks whether user answer corresponds to question answer"""
        if user_answer.lower() == question_answer.lower():
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong...")
        print(f"The correct answer was: {question_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number}")
        print("\n")