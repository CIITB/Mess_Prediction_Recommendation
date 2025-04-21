from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class AttendancePredictor(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=111, random_state=2)
        self.day_encoder = LabelEncoder()
        self.meal_encoder = LabelEncoder()
        self.menu_encoder = LabelEncoder()
        self.df = None

    def fit(self, df):
        """Trains the model with encoders"""
        self.df = df.copy()
        # Fit encoders
        self.df['Day_enc'] = self.day_encoder.fit_transform(df['Day'])
        self.df['Meal_enc'] = self.meal_encoder.fit_transform(df['Meal'])
        self.df['Menu_enc'] = self.menu_encoder.fit_transform(df['Menu_Item'])
        
        X = self.df[['Day_enc', 'Meal_enc', 'Menu_enc']]
        y = self.df['Attendance']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.15, random_state=2
        )
        self.model.fit(X_train, y_train)
        return self

    def predict(self, X):
        """Makes predictions"""
        return self.model.predict(X)

    def recommend_action(self, day, meal, menu_item):
        """Generates recommendations"""
        try:
            day_enc = self.day_encoder.transform([day])[0]
            meal_enc = self.meal_encoder.transform([meal])[0]
            menu_enc = self.menu_encoder.transform([menu_item])[0]
        except ValueError as e:
            raise ValueError(f"Invalid input value: {str(e)}")

        pred_attendance = self.model.predict([[day_enc, meal_enc, menu_enc]])[0]
        
        threshold = 90
        if pred_attendance < threshold:
            # Get alternatives from same meal type
            alternatives = self.df[
                (self.df['Meal_enc'] == meal_enc) & 
                (self.df['Menu_enc'] != menu_enc)
            ]
            alt_means = alternatives.groupby('Menu_Item')['Attendance'].mean()
            top_3 = alt_means.nlargest(3).index.tolist()
            return {
                'predicted_attendance': float(pred_attendance),
                'action': 'Suggest alternatives',
                'recommendations': top_3
            }
        else:
            return {
                'predicted_attendance': float(pred_attendance),
                'action': 'Keep current menu',
                'recommendations': []
            }
