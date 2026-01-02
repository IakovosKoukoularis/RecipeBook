# RecipeBook Manager 👨‍🍳📖

> A desktop application for managing culinary recipes, developed with Python and Tkinter.

<img width="674" height="624" alt="RecipeBook" src="https://github.com/user-attachments/assets/0a3d8da1-2682-4083-ae77-029da45f2175" />


## 📖 About
**RecipeBook Manager** is a GUI-based desktop application designed to help users organize their recipe collection efficiently. It offers full CRUD (Create, Read, Update, Delete) functionality, along with search capabilities and data backup features.

This project was developed as part of the **"Introduction to Software Engineering (PLHPRO)"** curriculum at the **Hellenic Open University (HOU)**, demonstrating proficiency in:
* Python Object-Oriented Programming (OOP).
* GUI development using **Tkinter**.
* File handling and Data Persistence (JSON/CSV).
* Algorithm implementation for searching and sorting data.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **GUI Framework:** Tkinter (Standard Python Interface)
* **Data Storage:** JSON / Text Files (Local Storage)
* **Tools:** VS Code, Git

## ✨ Key Features
Based on the project requirements, the application includes:
* ✅ **Recipe Management:** Add, Edit, and Delete recipes with details (Title, Ingredients, Execution, Category).
* ✅ **Smart Search:** Find recipes instantly by title or category.
* ✅ **Data Persistence:** Automatically saves recipes so data is never lost.
* ✅ **Import/Export:** Backup capability to export recipes to external files and import them back.
* ✅ **User-Friendly Interface:** Clean and intuitive graphical environment.

## 🚀 How to Run Locally

To run this application on your machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/IakovosKoukoularis/RecipeBook.git](https://github.com/IakovosKoukoularis/RecipeBook.git)
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd RecipeBook
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```
    *(Note: If your main file is named `gui.py` or `recipe_app.py`, replace `main.py` with the correct name).*

## 📂 Project Structure
```text
RecipeBook/
├── data/               # Folder storing recipe data files
├── images/             # Icons and UI assets
├── main.py             # Entry point of the application
├── recipe_class.py     # Class logic for Recipe objects
├── database.py         # Functions for file handling/saving
├── README.md           # Project documentation
└── requirements.txt    # Dependencies

## 📥 Download & Run (No Python required)

Want to try the app without installing Python?

1. Go to the **[Releases Page](https://github.com/IakovosKoukoularis/RecipeBook/releases)**.
2. Download the `RecipeBook.exe` file from the latest version.
3. Double-click to run!
   *(Note: Windows might warn you about an unrecognized app since it's not digitally signed. Click "More Info" -> "Run Anyway").*

Created by Iakovos Koukoularis

LinkedIn: linkedin.com/in/jack-koukoularis

GitHub: github.com/IakovosKoukoularis
