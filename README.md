## 🚀 Live Demo

You can access the deployed app here: [Mess Prediction & Recommendation App](https://mess-prediction-recommenda.onrender.com)

# **Smart Mess Menu Recommender**

## **Problem Statement**

This project aims to build a **Smart Mess Menu Recommender** system that helps students:  
1. Predict how likely people are to eat in the mess based on the day’s menu.  
2. Recommend whether to eat at the mess or skip it.  
3. Optionally, suggest better alternatives during low predicted attendance.

---

## **Approach**

Since the mess menu is fixed and rotates weekly, I generated a synthetic dataset based on three main features:
- **Day** (Monday to Sunday)
- **Meal** (Breakfast, Lunch, Snacks, Dinner)
- **Menu Items** (18 fixed dishes, repeated across different days/meals)

The target variable was **Attendance** (number of students likely to eat).

### **Feature Encoding**
- `Day`: encoded as ordinal numbers (0–6 for Mon–Sun)  
- `Meal`: encoded as categorical labels  
- `Menu Items`: encoded as categorical values (no OOV since menu is fixed)

### **Modeling**
- Used **Random Forest Regressor**, an ensemble learning method that handles non-linear relationships and categorical data effectively.
- Trained the model to predict attendance based on the day, meal type, and menu item.

### **Recommender System Logic**
- Once the predicted attendance (`y_pred`) is computed:
  - If `y_pred < 90`, the system recommends skipping the meal.
  - To suggest alternatives, the system:
    - Looks into the dataset to find all menus served for the same meal type across all days.
    - Calculates the mean attendance for each menu.
    - Recommends the top 3 menus based on popularity (attendance).
  - If `y_pred ≥ 90`, the meal is recommended as **worth eating**.

---

## **Setup Instructions**

To run the Smart Mess Menu Predictor & Recommender, follow these steps:

1. Download & Unzip the folder named `mess_predictor_and_recommender`.
2. It contains:
   - `Dataset (mess_data.csv)`
   - `Dataset generation script`
   - `Model training & prediction code`
   - A separate `model.api` folder for the API
3. Open the model training code and update the dataset path to match your local directory structure.
4. Run this script:
   - It will **train the model** using Random Forest Regressor.
   - Generate a serialized `model.pkl` file.
5. Navigate to the `model.api/` folder.
6. Replace the placeholder `model.pkl` with the newly generated one from the previous step.
7. Open the folder in VS Code (or any IDE).
8. Run the API:
   - In the terminal, execute: `python app.py`
9. If needed, adjust the library versions in `requirements.txt` to match your system.
10. Once the server starts, it will generate a local link.
11. Open the link in your browser.
12. Select the **Day**, **Meal**, and **Menu Item**.
13. It will:
    - Predict expected attendance.
    - Recommend whether to eat or skip.
    - Suggest better menu options.

---

## **Assumptions Made**

1. The mess menu remains unchanged and rotates on a fixed weekly basis.  
2. The maximum number of students that can eat in the mess is assumed to be **150**.  
3. A threshold of **90** is used to decide whether to recommend the meal.  
4. Only **18 distinct menu items** are included in the dataset.  
5. While the system is designed primarily for students to make dining decisions, it can also be beneficial for mess workers and administration:
   - Reducing food waste  
   - Planning meal preparations efficiently
