from flask import jsonify, make_response, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from .forms import LoginForm, RegistrationForm
from .models import Ops, OpsData, Region, User
from app import app, db
from .bussiness_logic import calculate_business_logic
from .loading_data import fill_ops, fill_ops_data, fill_podata_time


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ops_data_view'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("ops_data_view"))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('ops_data_view'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/")
@login_required
def ops_data_view():
    dictionary = {}
    ops_data = OpsData.query.all()
    for reg in Region.query.all():
        dictionary[reg.name] = []
        for ops in ops_data:
            if ops.region_id == reg.id:
                dictionary[reg.name].append(
                    {"sku": ops.sku, "total_units": ops.total_units}
                )
    return jsonify(dictionary)


@app.route("/ops")
def ops():
    arr = []
    reg_db = Region.query.all()
    for ops in Ops.query.all():
        arr.append(
            {
                "Buyer": ops.buyer,
                "SKU": ops.sku,
                "Ingredient": ops.ingredient,
                "Regions": calculate_business_logic(reg_db, ops),
            }
        )
    return jsonify(arr)


@app.route("/reload-data")
def reload_data():
    try:
        fill_ops()
        fill_ops_data()
        fill_podata_time()
    except Exception:
        return make_response(jsonify({"messages": "Error 500"}), 500)
    else:
        return make_response(jsonify({"messages": "Success"}), 200)


# class PostRegion(Resource):
#     def post(self):
#         try:
#             data = request.get_json(force=True)
#             name_of_region = data["name"]
#             obj = Region(name=name_of_region)
#             db.session.add(obj)
#             db.session.commit()
#             return make_response(jsonify({"msg":"success"}), 200)
#         except Exception:
#             return make_response(jsonify({"msg": "Error 500"}), 500)
