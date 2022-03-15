from tkinter import *
import copy
import random

root = Tk()

IMAGES = [
    {
        "name": "tree",
        "full": PhotoImage(file="images/tree.png"),
        "re5": PhotoImage(file="images/tree.png").subsample(5, 5)
    },
    {
        "name": "star",
        "full": PhotoImage(file="images/star.png"),
        "re5": PhotoImage(file="images/star.png").subsample(5, 5)
    },
    {
        "name": "red",
        "full": PhotoImage(file="images/b-red.png"),
        "re5": PhotoImage(file="images/b-red.png").subsample(5, 5)
    },
    {
        "name": "green",
        "full": PhotoImage(file="images/b-green.png"),
        "re5": PhotoImage(file="images/b-green.png").subsample(5, 5)
    },
    {
        "name": "blue",
        "full": PhotoImage(file="images/b-blue.png"),
        "re5": PhotoImage(file="images/b-blue.png").subsample(5, 5)
    },
    {
        "name": "orange",
        "full": PhotoImage(file="images/b-orange.png"),
        "re5": PhotoImage(file="images/b-orange.png").subsample(5, 5)
    }
]

PIVOT_POINTS = [
    [225, 40], # top
    [195, 145],
    [270, 220],
    [160, 270],
    [295, 305],
    [135, 350],
    [330, 390],
    [115, 445]
]
PIVOT_POINTS_5 = []
for pp in PIVOT_POINTS:
    PIVOT_POINTS_5.append([pp[0]/5, pp[1]/5])

CURRENT_ORDER = {"is_star": False, "balls": []}


def select_element(event):
    item_tags = canvas.gettags(CURRENT)

    if "is_move" in item_tags:
        canvas.addtag_withtag("active", CURRENT)
        canvas.dtag(CURRENT, "palette")

        canvas.delete("palette")
        draw_palette()

        canvas.bind("<Motion>", move_element)

def deselect_element(event):
    if not canvas.coords("active"): return
    r = 25
    x = canvas.coords("active")[0] + r
    y = canvas.coords("active")[1] + r

    cpp = None # closest pivot point

    for pp in PIVOT_POINTS:
        if (x - pp[0])**2 + (y - pp[1])**2 <= r**2:
            cpp = pp 

    if cpp is None:
        canvas.delete("active")
    else:
        canvas.coords("active", cpp[0]-r, cpp[1]-r)
        canvas.addtag_withtag("placed", CURRENT)
        canvas.dtag("active")
    
    canvas.unbind("<Motion>")
    canvas.delete("highlight")

def move_element(event):
    x = event.x
    y = event.y
    r = 25
    canvas.coords("active", x-r, y-r)

    cpp = None # closest pivot point

    for pp in PIVOT_POINTS:
        if (x - pp[0])**2 + (y - pp[1])**2 <= r**2:
            cpp = pp             
    
    if cpp is None:
        canvas.delete("highlight")
    else:
        canvas.create_oval(
            cpp[0]-r, cpp[1]-r,
            cpp[0]+r, cpp[1]+r,
            outline="red",
            tags=("highlight")
        )

def sell():
    elems = canvas.find_withtag("placed")
    answer = {"is_star": False, "balls": []}
    r = 25

    for el in list(elems):
        image_id = canvas.itemconfig(el)["image"][4]
        x = canvas.coords(el)[0] + r
        y = canvas.coords(el)[1] + r

        on_star = False
        for im in IMAGES[1:]:
            if image_id == str(im["full"]):
                if im["name"] == "star":
                    on_star = True
                    answer["is_star"] = True
                    break

                image_id = im["name"]

        if on_star: continue
        answer["balls"].append({
            "ball": image_id,
            "coords": [x, y]
        })

    on_star = answer["is_star"] == CURRENT_ORDER["is_star"]
    on_len = len(answer["balls"]) == len(CURRENT_ORDER["balls"])

    is_checked = on_star and on_len
    
    if is_checked:
        for b in CURRENT_ORDER["balls"]:
            if b not in answer["balls"]:
                is_checked = False
                break

    if is_checked:
        customer_wait()
        clear()

def clear():
    canvas.delete("placed")

def draw_palette():
    canvas.create_image(
        15, 10,
        anchor=NW, image=IMAGES[1]["full"], 
        tags=("is_move", "palette")
    )

    for i in range(len(IMAGES[2:])):
        bi = IMAGES[i+2]
        canvas.create_image(
            15, (i+1)*60 + 15,
            anchor=NW, image=bi["full"], 
            tags=("is_move", "palette")
        )

def draw_pivots():
    for p in PIVOT_POINTS:
        canvas.create_rectangle(
            p[0], p[1], 
            p[0]+2, p[1]+2, 
            outline="red", fill="red")

def remove_element(event):
    item_tags = canvas.gettags(CURRENT)

    if "is_move" in item_tags and "palette" not in item_tags:
        canvas.delete(CURRENT)
        canvas.delete("highlight")

def customer_wait():
    global CURRENT_ORDER
    order.delete("order")
    count = random.randint(1, len(PIVOT_POINTS))

    isStar = random.choice([True, False])
    CURRENT_ORDER["is_star"] = isStar

    if isStar:
        pps = PIVOT_POINTS_5[0]
        order.create_image(
            pps[0], pps[1],
            anchor=CENTER, image=IMAGES[1]["re5"], 
            tags=("order")
        )

        count -= 1

    CURRENT_ORDER["balls"] = []
    pivots = PIVOT_POINTS_5[1:].copy()
    for i in range(count):
        img = random.choice(IMAGES[2:])
        p = random.choice(pivots)

        pivots.pop(pivots.index(p))
        
        CURRENT_ORDER["balls"].append({
            "ball": img["name"],
            "coords": [p[0]*5, p[1]*5]
        })

        order.create_image(
            p[0], p[1],
            anchor=CENTER, image=img["re5"], 
            tags=("order")
        )

activities = Frame(root)

canvas = Canvas(
    activities, 
    width=IMAGES[0]["full"].width(), 
    height=IMAGES[0]["full"].height()
)
canvas.create_image(0,0,anchor=NW,image=IMAGES[0]["full"])

canvas.bind("<Button-1>", select_element)
canvas.bind("<Button-2>", remove_element)
canvas.bind("<ButtonRelease-1>", deselect_element)

draw_palette()
draw_pivots()

order = Canvas(
    activities, 
    width=IMAGES[0]["re5"].width(), 
    height=IMAGES[0]["re5"].height()
)

order.create_image(0,0,anchor=NW,image=IMAGES[0]["re5"])

controls = Frame(root)

clear_btn = Button(controls, text="clear", command=clear)
sell_btn = Button(controls, text="Sell!", command=sell)

canvas.grid(row=0, column=0)
order.grid(row=0, column=1)

clear_btn.grid(row=0, column=0)
sell_btn.grid(row=0, column=1)

activities.pack()
controls.pack()

customer_wait()
root.mainloop()