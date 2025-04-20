from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd


class AttendancePredictor:
    def __init__(temp):
        temp.model = RandomForestRegressor(n_estimators=111, random_state=2)
        temp.day = LabelEncoder()
        temp.meal = LabelEncoder()
        temp.menu = LabelEncoder()
        temp.df = None  

    def fit(temp, df):
        temp.df = df.copy()
        temp.df['Day_enc'] = temp.day.fit_transform(df['Day'])
        temp.df['Meal_enc'] = temp.meal.fit_transform(df['Meal'])
        temp.df['Menu_Item_enc'] = temp.menu.fit_transform(df['Menu_Item'])

        X = temp.df[['Day_enc', 'Meal_enc', 'Menu_Item_enc']]
        y = temp.df['Attendance']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=2)
        temp.model.fit(X_train, y_train)

        y_pred = temp.model.predict(X_test)
    
    def recommend_action(temp, day, meal, menu_item):
            
            day_enc = temp.day.transform([day])[0]
            meal_enc = temp.meal.transform([meal])[0]
            menu_enc = temp.menu.transform([menu_item])[0]

            pred_attendance = temp.model.predict([[day_enc, meal_enc, menu_enc]])[0]

            threshold = 90
            if pred_attendance < threshold:
                action = 'Suggest skipping or alternative options'

                alternatives = temp.df[(temp.df['Meal_enc'] == meal_enc) & (temp.df['Menu_Item_enc'] != menu_enc)]
                alt_mean_attendance = alternatives.groupby('Menu_Item')['Attendance'].mean().sort_values(ascending=False)
                top_alternatives = alt_mean_attendance.head(3).index.tolist()
            else:
                action = 'Attend'
                top_alternatives = []

            return {
                'predicted_attendance': float(pred_attendance),
                'action': action,
                'recommended_alternatives': top_alternatives
            }
meal_menu_mapping = {
    'Breakfast': ['PurBhaji', 'Dosa', 'Aloo Paratha', 'Upma', 'Idli-Sambhar', 'Poha'],
    'Lunch': ['Chole-Bhature', 'Dal Makhani', 'Chicken Biryani', 'Rajma-Chawal', 'Paneer Masala'],
    'Snacks': ['Sandwich', 'Cutlet', 'Tea-Pohe', 'Pakora', 'Samosa'],
    'Dinner': ['Paneer Butter Masala', 'Jeera Rice', 'Roti-Sabzi', 'Aloo Gobi', 'Dal-Chawal']
}



model = joblib.load('mess_model.pkl')


app = Flask(__name__)
from flask import Flask, render_template

@app.route('/')
def home():
    return render_template('index.html',menu_map=meal_menu_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    
        day = request.form['day']
        meal = request.form['meal']
        menu_item = request.form['menu_item']

        result = model.recommend_action(day, meal, menu_item)
        return render_template('index.html', prediction=result, menu_map=meal_menu_mapping)

        


if __name__ == '__main__':
    app.run(debug=True)
