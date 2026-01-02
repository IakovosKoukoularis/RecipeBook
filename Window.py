from tkinter import *
from tkinter import ttk #, messagebox, StringVar, IntVar, PhotoImage, Toplevel, Frame, Label, Tk, Button, Entry, OptionMenu, Listbox, Text, Canvas
from Recipe import Recipe
from Database import RecipeDB
import sqlite3

class MyWindow:

    def __init__(self, title, width, height, bgColor, iconFile):
        self.mainWindow = Tk()
        self.mainWindow.title(title)
        self.mainWindow.geometry(f"{width}x{height}")
        self.mainWindow.resizable(False,False)
        self.mainWindow.config(bg=bgColor)
        
        self.icon = PhotoImage(file=iconFile)
        self.mainWindow.iconphoto(False, self.icon)

        self.db = RecipeDB()
        self.recipes = self.db.load_recipes()

        self.creator = None

        self.menuPage()

    def clearWindow(self):
        for widget in self.mainWindow.winfo_children():
            widget.destroy()
        
    def menuPage(self):
        self.clearWindow()
        
        #Window Frames
        self.titleFrame = Frame(self.mainWindow, bg="#8a4036")
        self.titleFrame.pack(side="top", fill=None, expand=False)
        self.photoFrame = Frame(self.mainWindow, bg="#8a4036")
        self.photoFrame.pack(side="top", fill=None, expand=False)
        self.buttonFrame = Frame(self.mainWindow, bg="#3d3a37")
        self.buttonFrame.pack(side="top", fill=None, expand=False)
        self.emptyFrame = Frame(self.mainWindow, bg="#4a280f", height=600)
        self.emptyFrame.pack(side="top", fill="x", expand=True)
        #Header
        self.menuLabel = Label(self.titleFrame, text="Recipe Book",
                          font=("Impact",40), bg="#8a4036", fg="yellow")
        self.menuLabel.pack(pady=20)
        #Menu Image
        self.menuImage = PhotoImage(file = "main.png")
        self.menuPhoto = Label(self.photoFrame, image=self.menuImage, bg="black", borderwidth=6)
        self.menuPhoto.pack()
        #Buttons
        self.createButton = Button(self.buttonFrame, text="Add Recipe\n🔪",
                              width=20, height=3, 
                              font=("Impact",16), bg="#4f4e4d", fg="yellow", relief="raised",
                              command = self.recipeCreation)
        self.createButton.pack(side="left", padx=10)

        self.searchButton = Button(self.buttonFrame, text="Search Recipe\n📕",
                              width=20, height=3,
                              font=("Impact",16), bg="#4f4e4d", fg="yellow", relief="raised",
                              command = self.recipeSearch)
        self.searchButton.pack(side="left", padx=10)

    def recipeCreation(self):
        self.clearWindow()
        #Frames
        self.titleFrame = Frame(self.mainWindow, bg="#8a4036")
        self.titleFrame.grid(row=0,column=0,pady=2,sticky="n")
        self.entryFrame = Frame(self.mainWindow, border=5, bg="#616161", relief="ridge")
        self.entryFrame.grid(row=1,column=0,sticky="")
        self.buttonFrame = Frame(self.mainWindow, bg="#8a4036")
        self.buttonFrame.grid(row=2,column=0,sticky="ew")
        #Grid customisation
        self.mainWindow.grid_columnconfigure(0, weight=1) #Centers the grid
        self.buttonFrame.grid_columnconfigure(0, weight=1) #Create 3 columns for better customisation
        self.buttonFrame.grid_columnconfigure(1, weight=1)
        self.buttonFrame.grid_columnconfigure(2, weight=1)
        #Header
        self.addLabel=Label(self.titleFrame,text="Recipe Creation", font=("Impact",40), bg="#8a4036", fg="#f4fc00")
        self.addLabel.grid(row=0,column=0,pady=2,sticky="n")
        #Add Name
        self.nameLabel=Label(self.entryFrame,text="Name", font=("Impact",12), bg="#616161")
        self.nameLabel.grid(row=0,column=0,sticky="n",pady=2)
        self.nameEntry=Entry(self.entryFrame, font=("Impact",12),bg="#b8bfba")
        self.nameEntry.grid(row=1,column=0,sticky="n")
        #Add Category
        self.categoryLabel=Label(self.entryFrame,text="Category", font=("Impact",12), bg="#616161")
        self.categoryLabel.grid(row=2,column=0,sticky="n")
        self.categoryEntry=Entry(self.entryFrame, font=("Impact",12), bg="#b8bfba")
        self.categoryEntry.grid(row=3,column=0,pady=5,sticky="n")
        #Add Difficulty
        self.difficultyLabel=Label(self.entryFrame, text="Difficulty", font=("Impact",12), bg="#616161")
        self.difficultyLabel.grid(row=0,column=1,sticky="n")

        self.clicked = StringVar()
        self.clicked.set("Easy")
        self.difficultyEntry=OptionMenu(self.entryFrame, self.clicked, "Easy", "Medium", "Hard")
        self.difficultyEntry.config(width=8, border=3, highlightbackground="#616161", font=("Impact",12), bg="#9c9a95")
        self.difficultyEntry.grid(row=1,column=1,sticky="n",padx=10)
        #Hours
        self.hoursLabel=Label(self.entryFrame, text="Hours", font=("Impact",12), bg="#616161")
        self.hoursLabel.grid(row=0,column=2,sticky="n")

        self.hoursClicked = IntVar()
        self.hoursClicked.set(0)
        self.hoursEntry=OptionMenu(self.entryFrame, self.hoursClicked, 0,1,2,3,4,5,
                              command= lambda _: self.creator.confirmState())
        self.hoursEntry.config(width=2, border=3, highlightbackground="#616161", font=("Impact",12), bg="#9c9a95", padx=5)
        self.hoursEntry.grid(row=1,column=2,sticky="n")
        #Minutes
        self.minutesLabel=Label(self.entryFrame, text="Minutes", font=("Impact",12), bg="#616161")
        self.minutesLabel.grid(row=0,column=3,sticky="n")

        self.minutesClicked = IntVar()
        self.minutesClicked.set(0)
        self.minutesEntry=OptionMenu(self.entryFrame, self.minutesClicked, 0,5,10,15,20,25,30,35,40,45,50,55,59,
                                command= lambda _: self.creator.confirmState())
        self.minutesEntry.config(highlightbackground="#616161", width=2, border=3, font=("Impact",12), bg="#9c9a95", padx=5)
        self.minutesEntry.grid(row=1,column=3,sticky="n",padx=20)
        #Add and Delete Ingredients
        self.ingredientLabel=Label(self.entryFrame, text="Ingredients", font=("Impact"), bg="#616161")
        self.ingredientLabel.grid(row=5,column=0,pady=10,sticky="n")

        self.deleteIngredientButton=Button(self.entryFrame, text="❌", width=5, border=3, font=("Impact",10), bg="#9c9a95", fg="red")
        self.deleteIngredientButton.grid(row=5,column=0,padx=10,sticky="w")
        self.addIngredientButton=Button(self.entryFrame, text="✏️", width=5, border=3, font=("Impact",10), bg="#9c9a95", fg="blue")
        self.addIngredientButton.grid(row=5,column=0,padx=10,sticky="e")

        self.ingredientEntry=Entry(self.entryFrame, font="Georgia", bg="#b8bfba", fg="#02175c")
        self.ingredientEntry.grid(row=6,column=0,pady=5,padx=10,sticky="w")
        self.ingredientListbox=Listbox(self.entryFrame, font="Georgia", height=15, bg="#e6e1ac", fg="#02175c",relief="flat")
        self.ingredientListbox.grid(row=7,column=0,padx=10,sticky="w")
        #Add Steps Delete Steps
        self.stepLabel=Label(self.entryFrame, text="Steps", font=("Impact"), bg="#616161")
        self.stepLabel.grid(row=5,column=1,pady=10,sticky="n")

        self.deleteStepButton=Button(self.entryFrame, text="❌", width=5, border=3, font=("Impact",10), bg="#9c9a95", fg="red")
        self.deleteStepButton.grid(row=5,column=1,padx=10,sticky="w")
        self.addStepButton=Button(self.entryFrame, text="✏️", width=5, border=3, font=("Impact",10), bg="#9c9a95", fg="blue")
        self.addStepButton.grid(row=5,column=1,padx=10,sticky="e")

        self.stepEntry=Entry(self.entryFrame, font=("Georgia"), bg="#b8bfba", fg="#02175c")
        self.stepEntry.grid(row=6,column=1,pady=5,padx=10,sticky="w")
        #Step Duration
        self.durationLabel=Label(self.entryFrame, text="⏱️", font=("Arial",15,"bold"), bg="#616161")
        self.durationLabel.grid(row=6,column=2,sticky="w")
        self.durationEntry=Entry(self.entryFrame, font=("Georgia"), bg="#b8bfba", fg="#02175c")
        self.durationEntry.grid(row=6,column=1,pady=5,sticky="e")
        self.durationEntry.config(width=2)

        self.stepListbox=Listbox(self.entryFrame, width=23, height=15, font=("Georgia"), bg="#e6e1ac", fg="#02175c", relief="flat")
        self.stepListbox.grid(row=7,column=1,padx=10,sticky="w")
        #Confirmation Button
        self.confirm=Button(self.buttonFrame, text="Save Recipe\n💾", width=20, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised", state="disabled")
        self.confirm.grid(row=0,column=1,sticky="e",padx=100)
        #Return Button
        self.goBack=Button(self.buttonFrame,text="Go Back\n⬅️", width=20, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised")
        self.goBack.grid(row=0,column=1,sticky="w",padx=100)

        self.creator = Recipe(
            ingredientEntry = self.ingredientEntry,
            ingredientListbox = self.ingredientListbox,
            nameEntry = self.nameEntry,
            categoryEntry = self.categoryEntry,
            minutesClicked = self.minutesClicked,
            hoursClicked = self.hoursClicked,
            confirm = self.confirm,
            stepEntry = self.stepEntry,
            durationEntry = self.durationEntry,
            stepListbox = self.stepListbox,
            clicked = self.clicked,
            descriptionEntry = self.descriptionWindow,
            db = self.db
        )
        
        #Buttons
        self.deleteIngredientButton.config(command = self.creator.deleteIngredient)
        self.addIngredientButton.config(command = self.creator.addIngredient)
        self.deleteStepButton.config(command = self.creator.deleteStep)
        self.addStepButton.config(command = self.descriptionWindow)
        self.confirm.config(command = lambda: (self.creator.saveRecipe(), self.menuPage()))
        self.goBack.config(command = self.menuPage)
        #Bindings
        self.nameEntry.bind("<KeyRelease>", lambda e: self.creator.confirmState())
        self.categoryEntry.bind("<KeyRelease>", lambda e: self.creator.confirmState())

    def recipeCustomisation(self):
        self.clearWindow()
        self.recipeCreation() 
        # Φόρτωση των παλιών τιμών στα entry fields
        self.clicked.set(self.recipeInfo.get("values")[2])
        self.hoursClicked.set((self.recipeInfo.get("values")[3])//60)
        self.minutesClicked.set((self.recipeInfo.get("values")[3])%60)
        self.nameEntry.insert(0,self.recipeInfo.get("values")[0])
        self.categoryEntry.insert(0,self.recipeInfo.get("values")[1])

        # Φόρτωση των συστατικών
        ingredients_str = self.recipeInfo.get("values")[4]
        
        self.creator.ingredientList.clear()
        self.ingredientListbox.delete(0, "end")
        for item in ingredients_str.split(';'):
            if item: 
                self.creator.ingredientList.append(item)
                self.ingredientListbox.insert("end",f"{len(self.creator.ingredientList)}) {item}✔️")

        steps_data_str = self.recipeInfo.get("values")[5]
        self.creator.stepList.clear()
        self.creator.durationList.clear()
        self.creator.descriptionList.clear()
        self.stepListbox.delete(0, "end")
        
        try:
            steps_data_dict = eval(steps_data_str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse steps data: {e}")
            steps_data_dict = {}
            
        for i in sorted(steps_data_dict.keys()):
            step_info = steps_data_dict[i]
            title = step_info["Title"]
            duration = step_info["Duration"]
            description = step_info["Description"]
            
            self.creator.stepList.append(title)
            self.creator.durationList.append(duration)
            self.creator.descriptionList.append(description)
            self.stepListbox.insert("end", f"{len(self.creator.stepList)}) {title} | {duration}⏰")
        
        # Ενημέρωση της κατάστασης του confirm button
        self.goBack.config(command = self.recipeSearch)
        self.creator.confirmState()

    def checkState(self):
        if self.descriptionEntry.get("1.0","end-1c"):
            self.descriptionButton.config(state="normal")
        else:
            self.descriptionButton.config(state="disabled")

    def descriptionWindow(self):
        if len(self.stepEntry.get())>0:
            if self.stepEntry.get().isdigit():
                messagebox.showerror(title= "Error", message=f"{self.stepEntry.get()} is not valid")
                return
            if not 0<len(self.durationEntry.get())<3:
                messagebox.showerror(title= "Error", message=f"{self.durationEntry.get()} is not valid or empry")
                return
            if not self.durationEntry.get().isdigit():
                messagebox.showerror(title= "Error", message="Duration needs to be a digit")
                return
            if self.stepEntry.get().capitalize() in self.creator.stepList:
                messagebox.showerror(title= "Error", message="Step already exists")
                return
            else:
                self.creator.addStep()
                self.addStepButton.config(state="disabled")
                self.deleteStepButton.config(state="disabled")
                myToplevel = Toplevel(self.mainWindow)
                myToplevel.geometry("500x400")
                myToplevel.title("Add description")
                myToplevel.resizable(False,False)
                myToplevel.config(bg="#8a4036")
                myToplevel.protocol("WM_DELETE_WINDOW", "Unavailable")

                icon = PhotoImage(file="icon.png")
                myToplevel.iconphoto(False, icon)
                #TopLevel Entry
                self.descriptionEntry = Text(myToplevel, height=10, bg="#e6e1ac", fg="#02175c")
                self.descriptionEntry.pack()
                self.descriptionEntry.bind("<KeyRelease>", lambda _: self.checkState())
                #TopLevel Confirm Button
                self.descriptionButton = Button(myToplevel,text="Done",command= lambda: (self.creator.saveDescription(self.descriptionEntry), myToplevel.destroy(),
                                                                                        self.addStepButton.config(state="normal"), self.deleteStepButton.config(state="normal")))
                self.descriptionButton.config(state="disabled")
                self.descriptionButton.pack()
        else:
            messagebox.showerror(title= "Error", message="Cannot be empty")
            return

    def recipeSearch(self):
        self.clearWindow()
        self.titleFrame = Frame(self.mainWindow,bg="#8a4036")
        self.titleFrame.pack(fill=None, side="top",expand=False)
        self.buttonFrame = Frame(self.mainWindow)
        self.buttonFrame.pack(fill="x", side="top",expand=False)
        self.treeFrame = Frame(self.mainWindow)
        self.treeFrame.pack(fill="x", side="top",expand=False)

        Label(self.titleFrame, text="My recipes", font="Impact 40", bg="#8a4036", fg="#f4fc00").pack(pady=20)
        #Widgets
        self.searchButton = Button(self.buttonFrame,text="Search", width=10, bg="#2a2747", fg="yellow", relief="raised")
        self.searchButton.pack(side="left",padx=5)
        self.searchEntry = Entry(self.buttonFrame, width=30)
        self.searchEntry.pack(side="left",padx=5)
        self.filterButton = Button(self.buttonFrame,text="Filter", bg="#2a2747", fg="yellow", relief="raised")
        self.filterButton.pack(side="left",padx=5)
        
        # Filter Frame (initially hidden)
        self.filterFrame = Frame(self.mainWindow, bg="#3d3a37")
        # Pack later so it doesnt show

        # Filter Widgets inside filterFrame
        self.categoryFilterLabel = Label(self.filterFrame, text="Category:", bg="#3d3a37", fg="yellow")
        self.categoryFilterLabel.pack(side="left", padx=(10, 0))
        self.filterCategoryClicked = StringVar()
        self.filterCategoryClicked.set("Any") # Default filter option
        self.categoryFilterOptionMenu = OptionMenu(self.filterFrame, self.filterCategoryClicked, "Any", "Appetizer", "Main", "Salad", "Dessert", "Beverage", "Other")
        self.categoryFilterOptionMenu.config(width=10, bg="#9c9a95")
        self.categoryFilterOptionMenu.pack(side="left", padx=5)

        self.difficultyFilterLabel = Label(self.filterFrame, text="Difficulty:", bg="#3d3a37", fg="yellow")
        self.difficultyFilterLabel.pack(side="left", padx=(10, 0))
        self.filterDifficultyClicked = StringVar()
        self.filterDifficultyClicked.set("Any") # Default filter option
        self.difficultyFilterOptionMenu = OptionMenu(self.filterFrame, self.filterDifficultyClicked, "Any", "Easy", "Medium", "Hard")
        self.difficultyFilterOptionMenu.config(width=8, bg="#9c9a95")
        self.difficultyFilterOptionMenu.pack(side="left", padx=5)

        self.timeFilterLabel = Label(self.filterFrame, text="Max Time (min):", bg="#3d3a37", fg="yellow")
        self.timeFilterLabel.pack(side="left", padx=(10, 0))
        self.timeFilterEntry = Entry(self.filterFrame, width=5)
        self.timeFilterEntry.pack(side="left", padx=5)

        self.applyFilterButton = Button(self.filterFrame, text="Apply Filter", bg="#2a2747", fg="yellow", relief="raised", command=self.perform_filter)
        self.applyFilterButton.pack(side="left", padx=10)
        #Buttons
        self.customiseButton = Button(self.buttonFrame,text="Customise", width=10, bg="#2a2747", fg="yellow", relief="raised", command=self.recipeCustomisation)
        self.customiseButton.pack(side="left",padx=5)
        self.deleteButton = Button(self.buttonFrame,text="Delete", width=10, bg="#2a2747", fg="yellow", relief="raised", command=self.deleteRecipe)
        self.deleteButton.pack(side="left",padx=5)
        self.executeButton = Button(self.buttonFrame,text="Execute", width=10, bg="#2a2747", fg="yellow", relief="raised",command = self.executeRecipe)
        self.executeButton.pack(side="right",padx=5)
        self.current_step_index = 1 # added (Για να εχω το index 1 καθε φορα που γινεται η εκτελεση συνταγης. Το αρχικοποιω εδω γιατι παντα περναει απο το searchRecipe πριν γινει εκτελεση)
        self.myText= "No recipe"
        self.selectedLabel = Label(self.buttonFrame, text=self.myText, width=20)
        self.selectedLabel.pack(side="right",padx=5)
        #Button Commands
        self.searchButton.config(command=self.perform_search)
        self.filterButton.config(command=self.toggle_filter_options)
        self.customiseButton.config(state="disabled")
        self.deleteButton.config(state="disabled")
        self.executeButton.config(state="disabled")
        #Treeview Style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",background="silver",fieldbackground="silver",font=("Georgia",12))
        self.style.configure("Treeview.Heading",background="#9c9c9c",font=("Impact",14))
        #Treeview
        columnNames= ("Recipe 🍝","Category 🥩","Difficulty 🍔","Time ⏲️")
        self.treeview = ttk.Treeview(self.treeFrame,height=25,columns=columnNames,show="headings",selectmode= "browse")
        #Headings - Columns
        for col in columnNames:
            self.treeview.heading(col,text=col)
            self.treeview.column(col,anchor="center")

        self.treeview.pack(fill="both", expand = True)
        #Treeview Values
        try:
            with sqlite3.connect("Recipes.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name, category, difficulty, time ,ingredients, steps FROM recipes ORDER BY name")
                recipes = cursor.fetchall() # Μαζευει ολες τις συνταγες σε μια λιστα οπου στην οποια καθε συνταγη ειναι ενα tuple
                
                for recipe in recipes:
                    self.treeview.insert("", "end", values=recipe)
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load recipes: {e}")
    
        self.treeview.pack(fill="both", expand=True)
        #Events
        self.treeview.bind("<<TreeviewSelect>>", self.getSelection)
        #Return Button
        self.goBack=Button(self.mainWindow,text="Go Back\n⬅️", width=20, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised")
        self.goBack.pack(side="bottom")
        self.goBack.config(command = self.menuPage)  

    def deleteRecipe(self):
        selectedItem = self.treeview.selection()
            
        recipe_name = self.treeview.item(selectedItem)['values'][0]

        if messagebox.askyesno(title="Confirmation", message=f"Are you sure you want to delete:\n{recipe_name}?"):
            if self.db.delete_recipe(recipe_name):
                self.treeview.delete(selectedItem) # Διαγραφω απο το treeview
                self.recipes = self.db.load_recipes() # Ανανεωνει τις συνταγες
                messagebox.showinfo(title="Success", message=f"{recipe_name} successfully deleted")

    def executeRecipe(self):
        self.clearWindow()
        self.recipes = self.db.load_recipes() # Κανει update τις συνταγες απο την βαση
        
        bg_color = "#8a4036"
        bar_bg = "#B0B0B0"
        bar_fg = "#1D7300"

        self.title_label = Label(self.mainWindow, text=f"{self.current_recipe}", font=("Impact", 40),bg="#8a4036",fg='yellow')
        self.title_label.pack(pady=20,fill="x")

        newFrame = Frame(self.mainWindow,bg="#572922")
        newFrame.pack()
 
        # Creating dictionary from string
        step_dict = {}
        for item in str(self.recipes[self.current_recipe]['Steps'])[1:-1].split("}, "): # Επρεπε να γινει string 
            if not item.endswith("}"): item += "}"
            k, v = item.split(":", 1)
            k = int(k.strip())
            v = v.strip()[1:-1]
            inner = {}
            for pair in v.split(", '"):
                pk, pv = pair.split(":", 1)
                inner[pk.strip().strip("'")] = pv.strip().strip("'")
            step_dict[k] = inner

        if self.current_step_index <= len(step_dict): # If recipe steps are not completed

             # Time labels
            self.time_label0 = Label(newFrame, text="Step Duration", font=("Impact", 18), bg="#4f4e4d", fg="yellow", width=10)
            self.time_label0.pack(pady=(10, 0),fill="x")

            self.time_label = Label(newFrame, text=f"{step_dict[self.current_step_index]['Duration']} minutes", font=("Impact", 14), bg="#572922", fg="white")
            self.time_label.pack(pady=(0, 20),fill="both")

            self.ingredients_label = Label(newFrame, text=f"{self.current_recipe} - Ingredients", font=("Impact", 18), bg="#4f4e4d", fg="yellow")
            self.ingredients_label.pack(fill="x")

            # Joining multiple strings from list
            elements = str(self.recipes[self.current_recipe]['Ingredients']).strip("[]") # Επρεπε να γινει string
            elements = elements.replace("'", "")
            elements_list = elements.split(", ")
            ingredients_list = ', '.join(elements_list)

            # Ingredients and Step labels
            self.ingredients_box = Text(newFrame, height=4, width=40, font=("Georgia", 14), bg="#572922", fg="white", relief="flat", wrap="word")
            self.ingredients_box.insert("end", ingredients_list)
            self.ingredients_box.config(state="disabled")
            self.ingredients_box.pack(fill="x")

            self.stepTitle = step_dict[self.current_step_index]["Title"]
            self.step_label0 = Label(newFrame, text=f"{step_dict[self.current_step_index]["Title"]}", font=("Impact", 18), bg="#4f4e4d", fg="yellow")
            self.step_label0.pack(pady=(20, 0),fill="x")

            self.step_label = Text(newFrame, height=6, width=60, font=("Georgia", 14), bg="#572922", fg="white", relief="flat", wrap="word")
            self.stepDesctription = step_dict[self.current_step_index]["Description"]
            self.step_label.insert("end", f"{self.stepDesctription}")
            self.step_label.config(state="disabled")
            self.step_label.pack(fill="x")

            # Progress bar labels
            sum_duration = 0
            self.recipes[self.current_recipe]["Time"]
            if self.current_step_index == 1:
                self.progress_label = Label(newFrame, text="Progress: 0%", font=("Impact", 14), bg="#572922", fg="white", width=30)
                self.progress_label.pack(pady=(10, 0))
            else:
                
                for i in range(1,self.current_step_index):
                    sum_duration = sum_duration + int(step_dict[i]['Duration'])

                self.progress_label = Label(newFrame, text=f"Progress: {round(((sum_duration / self.recipes[self.current_recipe]["Time"]) * 100),2)}%", font=("Impact", 14), bg="#572922", fg="white", width=30)
                self.progress_label.pack(pady=(10, 0)) 
                              

            # Progress bar simulation
            self.progress_canvas = Canvas(newFrame, width=400, height=20, bg=bar_bg, highlightthickness=0)
            self.progress_canvas.pack(pady=(10,30))
            self.progress_canvas.create_rectangle(0, 0, (sum_duration / self.recipes[self.current_recipe]["Time"] * 100)*4, 20, fill=bar_fg, width=0)

            # Buttons
            self.button_frame = Frame(newFrame, bg="#572922")
            self.button_frame.pack(side='top', fill="x")

            if self.current_step_index <= len(step_dict)-1:
                self.next_button = Button(self.button_frame, text="Next Step\n→", width=50, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised",command=self.next_step)
                self.next_button.pack(side="right")
                self.previousButton = Button(self.button_frame, text="Previous Step\n←", width=50, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised",command=self.previousStep)
                self.previousButton.pack(side="left")
            else:
                self.next_button = Button(self.button_frame, text="Complete Recipe\n✅", width=50, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised",command=self.next_step)
                self.next_button.pack(side="right")
                self.previousButton = Button(self.button_frame, text="Previous Step\n←", width=50, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised",command=self.previousStep)
                self.previousButton.pack(side="left")#(anchor='center')              

            self.goBack = Button(self.mainWindow, text="Back to Search\n⬅️", width=20, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised")
            self.goBack.pack(side="bottom")
            self.goBack.config(command = self.recipeSearch)

        else: # When recipe steps are completed
            step_label = Label(self.mainWindow, text="Successfully Completed!\n\nAwesome Work!", font=("Arial", 20, "bold"), bg=bg_color, fg="white")
            step_label.pack(pady=(30, 30))
            self.goBack=Button(self.mainWindow,text="Back to Search\n⬅️", width=20, height=3, font=("Impact",10), bg="#2a2747", fg="yellow", relief="raised")
            self.goBack.pack(side="bottom")
            self.goBack.config(command = self.recipeSearch)

            progress_label = Label(self.mainWindow, text="Progress: 100%", font=("Impact", 14), bg=bg_color, fg="white")
            progress_label.pack(pady=(10, 0))
            progress_canvas = Canvas(self.mainWindow, width=400, height=20, bg=bar_bg, highlightthickness=0)
            progress_canvas.pack(pady=(0,0))
            progress_canvas.create_rectangle(0, 0, 400, 20, fill=bar_fg, width=0)
        
    def next_step(self):
        self.current_step_index += 1
        self.executeRecipe()

    def previousStep(self):
        if self.current_step_index > 1:
            self.current_step_index -= 1
            self.executeRecipe()
        
    def getSelection(self,_):
        self.customiseButton.config(state="normal")
        self.deleteButton.config(state="normal")
        self.executeButton.config(state="normal") # added (Για να μπορεις να πατησεις το execute μονο οταν επιλεξεις συνταγη)
    
        self.mySelection = self.treeview.selection()
        self.selectedItem = self.treeview.focus()
        self.recipeInfo = self.treeview.item(self.selectedItem)
        try:
            self.selectedLabel.config(text=self.recipeInfo.get("values")[0]) # Επιστρεφει μονο το ονομα της συνταγης
            
        except IndexError:
            self.selectedLabel.config(text="No Recipe")

            self.customiseButton.config(state="disabled")
            self.deleteButton.config(state="disabled")
            self.executeButton.config(state="disabled")
        self.current_recipe = self.selectedLabel['text'] # added (Για να εχω το ονομα της συνταγης και να το χρησιμοποιω σε αλλη μεθοδο. Προσπαθησα με το self.selectedLabel text αλλα ενω το εμφανιζει την πρωτη φορα μετα γινεται none οταν παω στο επομενο βημα της συνταγης γιατι δεν υπαρχει selectedlabel)

    def start(self):
        self.mainWindow.mainloop()

    def toggle_filter_options(self):
        """Toggles the visibility of the filter options frame."""
        if self.filterFrame.winfo_ismapped(): # Check if the frame is currently visible
            self.filterFrame.pack_forget() # Hide the frame
        else:
            self.filterFrame.pack(fill="x", side="top", expand=False) # Show the frame

    def perform_filter(self):
        """Performs filtering based on selected criteria."""
        category = self.filterCategoryClicked.get()
        difficulty = self.filterDifficultyClicked.get()
        max_time_str = self.timeFilterEntry.get()
        max_time = None

        if max_time_str:
            try:
                max_time = int(max_time_str)
            except ValueError:
                messagebox.showerror("Invalid input", "Max Time must be a number.")
                return

        filtered_recipes = self.db.filter_recipes(category=category, difficulty=difficulty, max_time=max_time)
        self.populate_treeview(filtered_recipes)

    def perform_search(self):

        # Select Recipe
        SelectedRecipe = self.searchEntry.get()
        
        # Search
        search_results = self.db.search_recipes(SelectedRecipe)
        self.populate_treeview(search_results)

    def populate_treeview(self, recipes=None):

        # Clear treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Update treeview
        if recipes is None:
            # If no recipes are provided, fetch all from the database
            try:
                with sqlite3.connect("Recipes.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, category, difficulty, time ,ingredients, steps FROM recipes ORDER BY name")
                    recipes = cursor.fetchall()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to load recipes: {e}")
                return

        for recipe in recipes:
            self.treeview.insert("", "end", values=recipe)

if __name__=="__main__":
    app = MyWindow("Recipe Book",900,800,"#8a4036","icon.png")
    app.start()