from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import pickle as pkl
import warnings
from datetime import datetime
from random import randrange as rn
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'hey'


with open(file="models/RandomForestRegressor_model.pkl", mode="rb") as file:
    model = pkl.load(file=file)


# def predict_label(img_path):
#     img = load_img(path=img_path, grayscale=False, color_mode='rgb', target_size=(128, 128))
#     img = img_to_array(img)
#     img = img / 255.0
#     img = np.expand_dims(img, axis=0)
#     model_prediction = model.predict(img)
#     model_label = np.argmax(model_prediction[0])
#     print("model predicted class : {}".format(model_label), "\n")
#     score = model_prediction[0][model_label]
#     acc = score * 100.0
#     print(acc)
#     predicted_class = df.loc[df["Class"] == model_label]["Formulas"][model_label]
#     print(predicted_class)
#     return predicted_class, acc


@app.route("/submit", methods=['GET', 'POST'])
def get_hours():
    if request.method == 'POST':
        junction_num = 0
        junction = request.form['junction']
        if junction == 'Water tank signal':
            junction_num = 0
        elif junction == 'bda signal':
            junction_num = 1
        elif junction == 'ayyappan signal':
            junction_num = 2
        elif junction == 'jonson hospital signal':
            junction_num = 3

        year = datetime.today().year
        month = datetime.today().month
        day = datetime.today().day

        r1 = rn(1, 3)
        r2 = rn(1, 6)
        df = pd.DataFrame(data=[junction_num, year, month, day, 0])
        print(df)
        df = df.T
        df.iloc[[0]].values
        model_prediction = model.predict(df.iloc[[0]])
        prediction = int(model_prediction)
        print(prediction)
        if r1 == 1:
            prediction += r2
        else:
            prediction -= r2
        print(prediction)
        if prediction <= 20:
            msg = "Detected as Less Traffic "
        elif 40 >= prediction > 20:
            msg = "Detected as Medium Traffic "
        else:
            msg = "Detected as heavy Traffic "
        return render_template("home.html", signal=junction, msg=msg, prediction=prediction)


@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form["email"]
        pwd = request.form["password"]
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["email"] == str(email) and row["password"] == str(pwd):
                return redirect(url_for('home'))
        else:
            mesg = 'Invalid Login Try Again'
            return render_template('login.html', msg=mesg)
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email']
        Password = request.form['Password']
        col_list = ["name", "email", "password"]
        r1 = pd.read_excel('user.xlsx', usecols=col_list)
        new_row = {'name': name, 'email': email, 'password': Password}
        r1 = r1.append(new_row, ignore_index=True)
        r1.to_excel('user.xlsx', index=False)
        print("Records created successfully")
        # msg = 'Entered Mail ID Already Existed'
        msg = 'Registration Successful !! U Can login Here !!!'
        return render_template('login.html', msg=msg)
    return render_template('login.html')


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/password', methods=['POST', 'GET'])
def password():
    if request.method == 'POST':
        current_pass = request.form['current']
        new_pass = request.form['new']
        verify_pass = request.form['verify']
        r1 = pd.read_excel('user.xlsx')
        for index, row in r1.iterrows():
            if row["password"] == str(current_pass):
                if new_pass == verify_pass:
                    r1.replace(to_replace=current_pass, value=verify_pass, inplace=True)
                    r1.to_excel("user.xlsx", index=False)
                    msg1 = 'Password changed successfully'
                    return render_template('password_change.html', msg1=msg1)
                else:
                    msg2 = 'Re-entered password is not matched'
                    return render_template('password_change.html', msg2=msg2)
        else:
            msg3 = 'Incorrect password'
            return render_template('password_change.html', msg3=msg3)
    return render_template('password_change.html')


@app.route('/graphs', methods=['POST', 'GET'])
def graphs():
    return render_template('graphs.html')


@app.route('/cnn')
def cnn():
    return render_template('cnn.html')


@app.route('/logout')
def logout():
    session.clear()
    msg = 'You are now logged out', 'success'
    return redirect(url_for('login', msg=msg))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
