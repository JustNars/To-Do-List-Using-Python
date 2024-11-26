from customtkinter import *
import json
from PIL import Image
import datetime


# Set appearance mode
set_appearance_mode("light")

class MainApp(CTk):
    def __init__(self):
        super().__init__()

        with open("Json-Files/app.json", "r") as file:
            data = json.load(file)
        self.geometry("740x600")
        self.title("Nar's To-Do List!")
        self.resizable(False, False)
        
        # images
        self.checked = CTkImage(Image.open(r"To-do-images\check.png"), size=(60, 60))
        self.plus = CTkImage(Image.open(r"To-do-images\to-do-list.png"), size=(28, 28))
        self.delete_img = CTkImage(Image.open(r"To-do-images\delete.png"), size=(20, 20))
        self.plus_thingy = CTkImage(Image.open(r"To-do-images\plus.png"), size=(20, 20))
        self.invaild = CTkImage(Image.open(r"To-do-images\incorrect.png"), size=(60, 60))
        self.das = CTkImage(Image.open(r"To-do-images\check-mark.png"), size=(28, 28))

        # frames
        self.frame = CTkFrame(self, corner_radius=20)
        self.frame.pack(pady=15, padx=15, fill="both", expand=True)
        self.len_frame = CTkFrame(self.frame, corner_radius=13, height=250, fg_color="#C91F37")
        self.len_frame.pack(padx=15, pady=15, side="bottom", fill="both")

        # Create scrollable frame
        self.scroll_frame = CTkScrollableFrame(self.frame, height=425, width=315, corner_radius=20)
        self.scroll_frame.place(x=20, y=20)

        # View done tasks button
        self.view_button = CTkButton(self.frame, text="View Done Tasks", image=self.das, font=("Arial", 20), corner_radius=10,
                                fg_color="#C91F37", command=self.view_done, hover_color="#B31C31", height=55,
                                width=295, compound="right")
        self.view_button.place(x=385, y=150)

        # labels that shows how many tasks the user has done and tasks they havent done
        # also shows todays date for some reason idk i was bored i guess.
        self.len_how_many_done_tasks = CTkLabel(self.len_frame, text=f"Done Tasks: \n{len(data["tasks_done"])}", font=("Arial", 23), text_color="white")
        self.len_how_many_done_tasks.pack(side="right", padx=15)
        self.len_how_many_to_do_tasks = CTkLabel(self.len_frame, text=f"To-Do Tasks: \n{len(data["tasks_to_do"])}", font=("Arial", 23), text_color="white")
        self.len_how_many_to_do_tasks.pack(side="left", padx=13)
        todays_date = CTkLabel(self.len_frame, text=datetime.date.today(), font=("Arial", 30), text_color="white")
        todays_date.pack(side="top", padx=13, pady=10)

        # Show Widgets
        self.show_widgets()

    def show_widgets(self):

        self.text_label = CTkLabel(self.frame, text="", font=("Arial", 22), image=None, compound="top")
        self.text_label.place(x=410, y=265)

        with open("Json-Files/app.json", "r") as file:
            data = json.load(file)

        self.view_button.configure(command=self.view_done, image=self.das, text="View Done Tasks")

         # entry widget
        self.enter_task_entry = CTkEntry(self.frame, placeholder_text="Add A Task", font=("Arial", 20), corner_radius=13,
                                    border_width=0, height=45, width=295)
        self.enter_task_entry.place(y=20, x=385)

        # Add task button
        add_task_button = CTkButton(self.frame, text="Add A Task", image=self.plus, font=("Arial", 20), corner_radius=10,
                                    fg_color="#C91F37", command=self.add_task, hover_color="#B31C31", height=55,
                                    width=295, compound="right")
        add_task_button.place(x=385, y=80)

        self.fill_scroll_frame()
        self.show_stats()

    def show_stats(self):
        with open(r"Json-Files/app.json", "r") as file:
            data = json.load(file)
        self.len_how_many_done_tasks.configure(text=f"Done Tasks: \n{len(data["tasks_done"])}")
        self.len_how_many_to_do_tasks.configure(text=f"To-Do Tasks: \n{len(data["tasks_to_do"])}")




    def add_task(self):
        with open(r"Json-Files/app.json", "r") as file:
            data = json.load(file)

        user_input = self.enter_task_entry.get().capitalize()

        # this if statement checks if the user typed in a task that
        # they already put in.
        if user_input in data["tasks_to_do"]:
            self.text_label.configure(text="Already In The To-Do List!", image=self.invaild)
            return
        else:
            self.text_label.configure(text="Added Task To To-Do List", image=self.checked)

        append_tasks = data["tasks_to_do"]
        append_tasks.append(str(user_input))

        with open(r"Json-Files/app.json", "w") as file:
            json.dump(data, file, indent=2)

        self.fill_scroll_frame()
        self.show_stats()

    def fill_scroll_frame(self):
        # this for loop destroys scroll_frames children..
        for children in self.scroll_frame.winfo_children():
            children.destroy()

        with open(r"Json-Files/app.json", "r") as file:
            data = json.load(file)

        tasks = data["tasks_to_do"]

        # this for loop just shows tasks that havent been done yet by using frames
        # and makes a button thats deletes (or done) a task.
        for i in range(len(tasks)):
            show_task_frame = CTkFrame(self.scroll_frame, corner_radius=20)
            show_task_frame.pack(side="top", pady=8)
            show_task_label = CTkLabel(show_task_frame, text=tasks[i], font=("Arial", 24))
            show_task_button = CTkButton(show_task_frame, text="", height=6, width=6, fg_color="#C91F37", hover_color="#B31C31",
                                                                # the i is the index
                                         command=lambda i=i: self.delete_task(i), image=self.delete_img, compound="top", corner_radius=20)
            if len(tasks[i]) >= 25:
                show_task_button.pack(side="bottom", padx=10)
                show_task_label.pack(side="left", padx=5)
            else:
                show_task_label.pack(side="left", padx=5)
                show_task_button.pack(side="right", padx=10)

        self.show_stats()



    def delete_task(self, index):
        
        with open(r"Json-Files/app.json", "r") as file:
            data = json.load(file)

        my_task = data["tasks_to_do"][index]
        data["tasks_done"].append(f"{my_task} - {datetime.date.today()}")

        del data["tasks_to_do"][index]

        with open(r"Json-Files/app.json", "w") as file:
            json.dump(data, file, indent=2)
            
        self.show_stats()
        self.fill_scroll_frame()


    # this func justs views the tasks the user has done.
    def view_done(self):
        for i in self.scroll_frame.winfo_children():
            i.destroy()

        with open(r"Json-Files/app.json", "r") as file:
            data = json.load(file)

        for i in data["tasks_done"]:
            show_done_label = CTkLabel(self.scroll_frame, text=i, font=("Arial", 24))
            show_done_label.pack(side="top", pady=8)

        self.view_button.configure(command=self.show_widgets, image=None, text="View To-Do List")

        
            


if __name__ == "__main__":
    MainApp().mainloop()