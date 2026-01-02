from Database import RecipeDB
from tkinter import messagebox

class Recipe:

    def __init__(self,ingredientEntry,ingredientListbox,nameEntry,categoryEntry,
                 minutesClicked,hoursClicked,confirm,stepEntry,durationEntry,
                 stepListbox,clicked,descriptionEntry,db=None):
        
        self.ingredientList, self.stepList, self.durationList, self.descriptionList = [], [], [], []
        self.steps = {}
        self.ingredientEntry = ingredientEntry
        self.ingredientListbox = ingredientListbox
        self.nameEntry = nameEntry
        self.categoryEntry = categoryEntry
        self.minutesClicked = minutesClicked
        self.hoursClicked = hoursClicked
        self.confirm = confirm
        self.stepEntry = stepEntry
        self.durationEntry = durationEntry
        self.stepListbox = stepListbox
        self.clicked = clicked
        self.descriptionEntry = descriptionEntry

        #Database
        self.db = RecipeDB()
        self.recipes = self.db.load_recipes()

    def confirmState(self,*_):
        #Ελεγχω οτι ολα τα πεδια εχουν τις τιμες που θελω 
        if len(self.nameEntry.get())>1 and len(self.categoryEntry.get())>1 and len(self.ingredientList)>1 and len(self.stepList)>1 and (len(self.descriptionList)==len(self.stepList)):
        
            if not self.nameEntry.get().isdigit() and not self.categoryEntry.get().isdigit():

                if self.timeCalculation() > 0:
                    self.confirm.config(state="normal")
                else:
                    self.confirm.config(state="disabled")
        else:
            self.confirm.config(state="disabled")

    def timeCalculation(self):
        return self.hoursClicked.get() * 60 + self.minutesClicked.get() if self.hoursClicked.get() > 0 else self.minutesClicked.get()

    def addIngredient(self):
        if (self.ingredientEntry.get().capitalize() not in self.ingredientList) and len(self.ingredientEntry.get())>1:

            if not self.ingredientEntry.get().isdigit():
                self.ingredientList.append(self.ingredientEntry.get().capitalize())
                self.ingredientListbox.insert("end",f"{len(self.ingredientList)}) {self.ingredientList[-1]}✔️") #Εμφανιζει το τελευταιο στοιχειο της λιστας στο listBox
                self.ingredientEntry.delete(0,"end") #Διαγραφει την λεξη απο το πεδιο ωστε να μην χρειαζεται να το κανει ο χρηστης χειροκινητα
                self.confirmState()

    def deleteIngredient(self):
          selected_indices = self.ingredientListbox.curselection()
          if selected_indices:
            # Διαγράφουμε από το Listbox και από τη λίστα, ξεκινώντας από το τέλος για να μην επηρεαστούν οι δείκτες
            for index in selected_indices[::-1]:
                self.ingredientListbox.delete(index)
                del self.ingredientList[index]
            
            # Ενημερώνουμε την αρίθμηση στο Listbox μετά τη διαγραφή
            self.ingredientListbox.delete(0, "end")
            for i, item in enumerate(self.ingredientList):
                self.ingredientListbox.insert("end", f"{i+1}) {item}✔️")
            
            self.confirmState()
          else:
            messagebox.showwarning(title="Warning", message="Select an ingredient to delete.")

    def addStep(self):
        if (self.stepEntry.get().capitalize() not in self.stepList) and len(self.stepEntry.get())>1:

            if not self.stepEntry.get().isdigit() and self.durationEntry.get().isdigit() and len(self.durationEntry.get())<=2 and int(self.durationEntry.get())>0:
                self.stepList.append(self.stepEntry.get().capitalize())
                self.durationList.append(self.durationEntry.get())
                self.stepListbox.insert("end",f"{len(self.stepList)}) {self.stepList[-1]}  | {self.durationList[-1]}⏰")
                self.stepEntry.delete(0,"end")
                self.durationEntry.delete(0,"end")
                self.confirmState()
        
    def deleteStep(self):
        selected_indices = self.stepListbox.curselection()
        if selected_indices:
            for index in selected_indices[::-1]:
                self.stepListbox.delete(index)
                del self.stepList[index]
                del self.durationList[index]
                del self.descriptionList[index] # Σημαντικό να διαγράφεται και η περιγραφή

            self.stepListbox.delete(0, "end")
            for i, (step, duration) in enumerate(zip(self.stepList, self.durationList)):
                self.stepListbox.insert("end", f"{i+1}) {step} | {duration}⏰")
            
            self.confirmState()
        else:
            messagebox.showwarning(title="Warning", message="Select a step to delete.")

    def saveDescription(self,myEntry):
        cleanString = myEntry.get("1.0","end-1c").replace("  ","").replace("\n"," ") #βγαζει τα εξτρα κενα και τα συμβολα αλλαγης σειρας
        self.descriptionList.append(cleanString.capitalize())
        self.confirmState()

    def saveStep(self):
        for i in range(len(self.stepList)):
            self.steps[i+1]={
                "Title": self.stepList[i],
                "Duration": self.durationList[i],
                "Description": self.descriptionList[i]
            }
        return self.steps

    def saveRecipe(self):
        
        if not self.nameEntry.get():
            messagebox.showwarning(title="Warning", message="Recipe name cannot be empty")
            return

        if self.nameEntry.get() in self.recipes:
            if not messagebox.askyesno(title="Confirmation", message="Recipe already exists.\nDo you want to overwrite?"):
                return
        
        recipe_data = {
            'Name': self.nameEntry.get().capitalize(),
            'Category': self.categoryEntry.get().capitalize(),
            'Difficulty': self.clicked.get(),
            'Time': self.timeCalculation(),
            'Ingredients': self.ingredientList,
            'Steps': self.saveStep()
        }

        if self.db.save_recipe(recipe_data):
            self.recipes = self.db.load_recipes()  # Ανανεωνει το λεξικο απο την βαση
            messagebox.showinfo(title="Success", message="Recipe saved successfully")
            return True
        return False