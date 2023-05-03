from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLUE = "#4390F8"
FONT_NAME = "Courier"
WORK_MIN = 20
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
count_down_timer = None
TIME_LEFT = 0

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(count_down_timer)
    timer.config(text='Timer')
    checked_mark.config(text='')
    canvas.itemconfig(timer_text, text='00:00')
    global reps
    reps = 0

# ---------------------------- UI SETUP ------------------------------- #


def pause_timer():
    global TIME_LEFT
    if pause_button['text'] == 'Pause':
        window.after_cancel(count_down_timer)
        minute, second = canvas.itemcget(timer_text, 'text').split(':')
        TIME_LEFT = int(minute) * 60 + int(second)
        pause_button.config(text="Resume")
    elif pause_button['text'] == 'Resume':
        count_down(TIME_LEFT)
        pause_button.config(text="Pause")
        TIME_LEFT = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def call_timer():
    global reps
    WORK_SEC = WORK_MIN * 60
    SHORT_SEC = SHORT_BREAK_MIN * 60
    LONG_SEC = LONG_BREAK_MIN * 60
    reps = reps + 1
    if reps % 8 == 0:
        timer.config(text='Break', fg=BLUE)
        count_down(LONG_SEC)
    elif reps % 2 == 0:
        timer.config(text='Break', fg=GREEN)
        count_down(SHORT_SEC)
    else:
        timer.config(text='Work')
        count_down(WORK_SEC)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    count_min = count//60
    count_seconds = count % 60
    if count_seconds in range(0, 10):
        count_seconds = '0' + str(count_seconds)
    canvas.itemconfig(timer_text, text=f'{count_min}:{count_seconds}')
    if count > 0:
        global count_down_timer
        count_down_timer = window.after(1000, count_down, count-1)
        count_down_timer
    else:
        if reps % 2 == 0:
            completed = int(reps/2) * '✅'
            checked_mark.config(text=completed)
        call_timer()
        # call_timer()

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Pomodoro")
window.config(padx=30, pady=30, bg=YELLOW)
window.minsize(height=100, width=100)

checked_mark = Label(window, bg=YELLOW,
                     fg=GREEN)
checked_mark.grid(column=1, row=4)

timer = Label(window, text='Timer', bg=YELLOW,
              fg=PINK, font=(FONT_NAME, 50))
timer.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = PhotoImage(file='tomato.png')
canvas.create_image(100, 112, image=img)
timer_text = canvas.create_text(100, 130, text='00:00', font=(
    FONT_NAME, 35, 'bold'), fill='white')
canvas.grid(column=1, row=1, pady=(0, 20))

start_button = Button(text='Start',
                      highlightbackground=YELLOW, command=call_timer)
start_button.grid(column=0, row=2)

pause_button = Button(text='Pause',
                      highlightbackground=YELLOW, command=pause_timer)
pause_button.grid(column=1, row=2)

reset_button = Button(text='Reset',
                      highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(column=2, row=2)


window.mainloop()
