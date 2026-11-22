# python-tkinter-quiz

NETQUIZ
 
Name: Azanelle G. Arcojada
Section: SE 3 - A
Topic: Networking
 
## Features Completed
  	10 multiple-choice questions
  	Random question order
  	15-second countdown timer
  	Answer checking and time-out handling
  	Score and percentage
  	Answer review
  	High score saved in a text file
  	Restart button
 
## How the Questions Are Stored and Shuffled
  The questions are stored in a list called QUESTIONS. Each question is a dictionary with the question, the four choices, and the letter    of the right answer. When the quiz starts or restarts, random.sample() makes a shuffled copy of the list so the order is different        every time. 

## How the Timer Works
Every question starts at 15 seconds. The program uses root.after(1000, update_timer) to lower the time by 1 every second and show it on the screen. When I click Submit, stop_timer() cancels the countdown, and if the time reaches 0, the question is marked wrong.
 
## How the Program Identifies the Correct Answer
  Each choice button holds its letter (A, B, C, or D), so the program knows which one I picked. When I click Submit, it checks if that     letter is the same as the answer letter saved in the question. If it is the same, the answer is correct. 

## How the Score and High Score Work
  The score goes up by 1 for every correct answer. The percentage is the score divided by 10, then multiplied by 100. The high score is     saved in high_score.txt, and the program only replaces it when my new score is higher. 


## Function Explanations
| Functions          | Purpose                                          | Called When                                 |
| start_quiz()       | Resets everything and shuffles the questions     | Start or Restart is clicked                 |
| update_timer()     | Shows the time left and counts down every second | A question is shown                         |
| stop_timer()       | Stops the countdown                              | An answer is submitted or the quiz restarts |
| submit_answer()    | Checks the answer and adds to the score          | Submit is clicked                           |
| time_up()          | Marks the question wrong when time runs out      | The timer reaches 0                         |
| get_high_score()   | Reads the high score from the text file          | The start screen opens                      |
| save_high_score()  | Saves the score if it is higher than the old one | The results screen is shown                 |
| show_results()     | Shows the score, percentage, message, and review | After question 10                           |

## Screenshots 
<img width="942" height="632" alt="start" src="https://github.com/user-attachments/assets/00645b3d-0f6d-4784-bcbc-c6d7e2a3113d" />
<img width="942" height="632" alt="question" src="https://github.com/user-attachments/assets/96381736-278b-4406-b63c-fa420bfa0e3a" />
<img width="942" height="632" alt="feedback" src="https://github.com/user-attachments/assets/635f64fb-6370-4d5f-bf91-aa38cd6c5d5b" />
<img width="942" height="632" alt="results" src="https://github.com/user-attachments/assets/107fecbb-68b2-4b84-8e24-bc29868a6eab" />
<img width="942" height="632" alt="high_score" src="https://github.com/user-attachments/assets/ff8755f7-66c6-4d9f-a885-1d8dd52a96a3" />

## Challenges I Faced
  How I store the score. And also the workflow of the program.






