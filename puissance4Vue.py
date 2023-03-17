from tkinter import Tk, Canvas, Frame, Label, OptionMenu, StringVar, Button
from proje import Board
from player import InterfacePlayer

# define the dimensions of the grid
num_columns = 7
num_rows = 6

# define the dimensions of each cell in the grid
cell_width = 40
cell_height = 40

root = Tk()
frm = Frame(root)
frm.grid()

cnv4 = Canvas(frm, width=600, height=150)
cnv4.grid(columnspan=3, row=1)
cnv4.pack_propagate(False)
cnv = Canvas(frm, width=400, height=300)
cnv.grid(column=1, row=0,padx=(130, 10))

stvar = StringVar()
stvar.set("MonteCarlo")

stvar2 = StringVar()
stvar2.set("MonteCarlo")

# draw the grid of rectangles
for i in range(num_rows):
    for j in range(num_columns):
        x1 = j * cell_width
        y1 = i * cell_height
        x2 = x1 + cell_width
        y2 = y1 + cell_height
        cnv.create_rectangle(x1, y1, x2, y2, fill="white")


def on_canvas_click(event):
    column = event.x // 40
    if board.checkWin() < 0:
        if isinstance(board.player, InterfacePlayer):
            if 0 <= column < 7 and board.firstfreerow[column] < board.rows:
                board.play(column + 1)
                board.print()
                row, col = board.lastplay
                num_joueur = board.player.number
                if num_joueur == 1:
                    cnv.create_oval((column * cell_width) + (cell_width / 2) - 15,
                                    ((5-row) * cell_height) + (cell_width / 2) - 15,
                                    (column * cell_width) + (cell_width / 2) + 15,
                                    ((5-row) * cell_height) + (cell_width / 2) + 15, fill="red")
                else:
                    cnv.create_oval((column * cell_width) + (cell_width / 2) - 15,
                                    ((5-row) * cell_height) + (cell_width / 2) - 15,
                                    (column * cell_width) + (cell_width / 2) + 15,
                                    ((5-row) * cell_height) + (cell_width / 2) + 15, fill="yellow")
            else:
                print("invalid move")
    else:
        print("Board is already final")
        return

    if board.checkWin() >= 0:
        print("Win : " + board.getOtherPlayerName())
        Label(cnv4,text="La partie est terminé " + board.getOtherPlayerName() + " est le gagnant").pack()
        return
    if board.turnplayed == board.cols * board.rows:
        print("Draw")
        return
    # print("Clicked on column:", column+1)


cnv.bind("<Button-1>", on_canvas_click)

def ValeurJ1():
    print(stvar.get())
def ValeurJ2():
    print(stvar2.get())

cnv2 = Canvas(frm, width=150, height=300)
cnv2.grid(column=0, row=0)
# create a label and add it to the second canvas
Label(cnv2, text="J1").pack(side="top")
MenuJ1 = OptionMenu(cnv2, stvar, "MonteCarlo", "MinMax", "Joueur humain")
MenuJ1.pack(side="top")
Button(cnv2, text="Jouer", command=ValeurJ1).pack(side="top")
# create a red circle below the button in the second canvas
x = 75  # x-coordinate of the center of the circle
y = 150  # y-coordinate of the center of the circle
r = 35  # radius of the circle
cnv2.create_oval(x - r, y - r, x + r, y + r, fill="red")

cnv3 = Canvas(frm, width=150, height=300)
cnv3.grid(column=2, row=0)
# create a label and add it to the second canvas
Label(cnv3, text="J2").pack(side="top")
menuJ2 = OptionMenu(cnv3, stvar2, "MonteCarlo", "MinMax", "Joueur humain")
menuJ2.pack(side="top")
Button(cnv3, text="Jouer", command=ValeurJ2).pack(side="top")
# create a red circle below the button in the second canvas
x = 75  # x-coordinate of the center of the circle
y = 150  # y-coordinate of the center of the circle
r = 35  # radius of the circle
cnv3.create_oval(x - r, y - r, x + r, y + r, fill="yellow")

cnv.pack_propagate(False)
cnv2.pack_propagate(False)
cnv3.pack_propagate(False)

board = Board(InterfacePlayer("Axel"), InterfacePlayer("Lexa"))

root.mainloop()
