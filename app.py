from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


# file_path = os.path.abspath(os.getcwd())+"\database.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/banks'
db = SQLAlchemy(app)


class Bank_details(db.Model):
    bank_id = db.Column(db.Integer(), primary_key=True)
    bank_name = db.Column(db.String(49),  nullable=True)
    bank_ifsc = db.Column(db.String(11),  nullable=True)
    bank_branch = db.Column(db.String(74),  nullable=True)
    bank_address = db.Column(db.String(195),  nullable=True)
    bank_city = db.Column(db.String(50),  nullable=True)
    bank_district = db.Column(db.String(50),  nullable=True)
    bank_state = db.Column(db.String(26),  nullable=True)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/bank-details", methods=['GET', 'POST'])
def bank_detail():
    if(request.method == 'POST'):
        ifsc_code = request.form.get('ifsc_code')
        print(ifsc_code)
        bank = Bank_details.query.filter_by(bank_ifsc=ifsc_code).first()
        print(bank)

        legend = "Search Results"
        return render_template('bank.html', legend=legend, bank=bank)

    return render_template('bank.html')


@app.route("/branchdetails", methods=['GET'])
def branchdetails():

    # # # Set the pagination configuration
    # page = request.args.get('page', 1, type=int)

    # if(request.method == 'POST'):
    #     bank_name = request.form.get('bank_name')
    #     bank_name = "%{0}%".format(bank_name)

    #     city_name = request.form.get('city_name')
    #     city_name = "%{0}%".format(city_name)

    #     per_page = int(request.form.get('offset'))

    #     branchdetails = Bank_details.query.filter(Bank_details.bank_name.like(bank_name),Bank_details.bank_city.like(city_name)).paginate(page,per_page,error_out=False)
    #     # print(result[0].bank_id)

    #     legend = "Search Results"
    #     return render_template('branch.html', legend = legend, branchdetails = branchdetails)

    return render_template('branch.html')


@app.route("/branchdetails/results", methods=['GET', 'POST'])
def results():

    page = request.args.get('page', 1, type=int)

    bank_name = request.form.get('bank_name')
    bank_name = "%{0}%".format(bank_name)

    city_name = request.form.get('city_name')
    city_name = "%{0}%".format(city_name)

    per_page = 5
    if per_page == None:
        per_page = 5
    else:    
        per_page = int(request.form.get('offset'))

    # print(bank_name)
    # print(city_name)
    # print(per_page)
    branchdetails = Bank_details.query.filter(Bank_details.bank_name.like(
        bank_name), Bank_details.bank_city.like(city_name)).paginate(page, per_page, error_out=False)

    return render_template('results.html', branchdetails=branchdetails)


app.run(debug=True)
