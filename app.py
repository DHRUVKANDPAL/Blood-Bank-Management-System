from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone  # Import timezone from datetime module
import pytz


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for session management

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    contact_details = db.Column(db.String(20))
    address = db.Column(db.String(100))
    blood_type = db.Column(db.String(5))
    medical_history = db.Column(db.Text)
    eligibility_for_donation = db.Column(db.Boolean, default=True)
    donations = db.relationship('DonationRecord', backref='user', lazy=True) 

class DonationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    donation_date = db.Column(db.Date, nullable=False, default='2000-01-01')  # Set a default date as string

class D_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    donation_date = db.Column(db.Date, nullable=False, default='2000-01-01')
    quantity = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)

class BloodInventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(5), nullable=False, unique=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    contact_details = db.Column(db.String(20))
    address = db.Column(db.String(100))
    blood_type = db.Column(db.String(5))
    medical_conditions = db.Column(db.Text)
    treatment_history = db.Column(db.Text)
    attending_physician = db.Column(db.String(50))



@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        gender = request.form['gender']
        date_of_birth_str = request.form['date_of_birth']  
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        contact_details = request.form['contact_details']
        address = request.form['address']
        blood_type = request.form['blood_type']
        medical_conditions = request.form['medical_conditions']
        treatment_history = request.form['treatment_history']
        attending_physician = request.form['attending_physician']

        new_patient = Patient(username=username, email=email, password=password, full_name=full_name,
                              gender=gender, date_of_birth=date_of_birth, contact_details=contact_details,
                              address=address, blood_type=blood_type, medical_conditions=medical_conditions,
                              treatment_history=treatment_history, attending_physician=attending_physician)


        db.session.add(new_patient)
        db.session.commit()

        flash('Patient added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_patient.html')

@app.route('/')
def index():
    users = User.query.all()
    app.logger.debug('Index route accessed')  
    return render_template('index.html', users=users)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        gender = request.form['gender']
        date_of_birth_str = request.form['date_of_birth']
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        contact_details = request.form['contact_details']
        blood_type = request.form['blood_type']
        medical_history = request.form['medical_history']

        new_user = User(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            gender=gender,
            date_of_birth=date_of_birth,
            contact_details=contact_details,
            blood_type=blood_type,
            medical_history=medical_history
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('donor_dashboard'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('donor_dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')  
    return redirect(url_for('index'))


@app.route('/edit_profile/<int:donor_id>', methods=['GET', 'POST'])
def edit_profile(donor_id):
    donor = User.query.get_or_404(donor_id)

    if request.method == 'POST':
        # Process the form data for editing profile
        donor.full_name = request.form['full_name']
        donor.gender = request.form['gender']

        # Convert the string to a Python date object
        donor.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

        donor.contact_details = request.form['contact_details']
        donor.address = request.form['address']
        donor.blood_type = request.form['blood_type']
        donor.medical_history = request.form['medical_history']

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('donor_dashboard'))

    return render_template('edit_profile.html', donor=donor, donor_id=donor_id)



@app.route('/loginpatient', methods=['GET', 'POST'])
def loginpatient():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if a patient with the provided username exists
        patient = Patient.query.filter_by(username=username,password=password).first()

        if patient :
            # Login the patient using Flask-Login
            session['user_id'] = patient.id
            session['user_type'] = 'patient'
            flash('Login successful!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('loginpatient.html')



@app.route('/edit_patient_profile/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient_profile(patient_id):
    # Fetch the patient from the database
    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        # Process the form data for editing patient profile
        patient.full_name = request.form['full_name']
        patient.gender = request.form['gender']

        # Convert the string to a Python date object
        patient.date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()

        patient.contact_details = request.form['contact_details']
        patient.address = request.form['address']
        patient.blood_type = request.form['blood_type']
        patient.medical_conditions = request.form['medical_conditions']
        patient.treatment_history = request.form['treatment_history']
        patient.attending_physician = request.form['attending_physician']

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_dashboard'))

    return render_template('edit_patient_profile.html', patient=patient, patient_id=patient_id)



@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the provided credentials are for an admin
        if username == 'admin@172' and password == '7896321450@CDDD':
            # Set a session variable to identify the user as an admin
            session['user_type'] = 'admin'
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')

    return render_template('loginadmin.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Donor List
@app.route('/donor_list')
def donor_list():
    users = User.query.all()
    return render_template('donor_list.html', users=users)

# Patient List
@app.route('/patient_list')
def patient_list():
    patients = Patient.query.all()
    return render_template('patient_list.html', patients=patients)


@app.route('/donor_dashboard')
def donor_dashboard():
    user_id = session.get('user_id')
    if user_id:
        donor = User.query.get(user_id)
        donation_records = D_record.query.filter_by(user_id=user_id).all()
        return render_template('donor_dashboard.html', donor=donor, donation_records=donation_records)
    else:
        flash('You need to log in as a donor.', 'danger')
        return redirect(url_for('login'))


@app.route('/donate', methods=['POST'])
def donate():
    if request.method == 'POST':
        donor_id = request.form.get('donor_id')
        quantity = request.form.get('quantity')
        donation_date_str = request.form.get('donation_date')

        # Fetch blood group from the session user's ID
        user = User.query.get(donor_id)
        blood_group = user.blood_type if user else None

        # Validate and process the donation
        if donor_id and quantity and donation_date_str and blood_group:
            # Convert donation_date to a Python date object
            donation_date = datetime.strptime(donation_date_str, '%Y-%m-%d').date()

            # Save the donation record to the database
            new_donation = D_record(user_id=donor_id, quantity=quantity, donation_date=donation_date, blood_group=blood_group)
            db.session.add(new_donation)
            db.session.commit()

            # Update the blood inventory
            update_blood_inventory(blood_group, quantity)

            flash('Donation successful!', 'success')
            return redirect(url_for('donor_dashboard'))
        else:
            flash('Invalid donation data. Please try again.', 'danger')
            return redirect(url_for('donor_dashboard'))

def update_blood_inventory(blood_group, quantity):
    # Fetch the current blood inventory from the database
    blood_inventory = BloodInventory.query.filter_by(blood_group=blood_group).first()

    # If the blood inventory doesn't exist, create a new record
    if not blood_inventory:
        blood_inventory = BloodInventory(blood_group=blood_group, quantity=quantity)
        db.session.add(blood_inventory)
    else:
        # Update the existing blood inventory
        quantity=int(quantity)
        blood_inventory.quantity += quantity

    # Commit the changes to the database
    db.session.commit()


@app.route('/blood_inventory')
def blood_inventory():
    # Fetch blood inventory data from the database
    blood_inventory_data = fetch_blood_inventory()
    return render_template('blood_inventory.html', blood_inventory=blood_inventory_data)

def fetch_blood_inventory():
    blood_inventory_data = {}
    inventory_records = BloodInventory.query.all()

    for record in inventory_records:
        blood_inventory_data[record.blood_group] = record.quantity

    return blood_inventory_data

def get_donation_records(user_id):
    return D_record.query.filter_by(user_id=user_id).all()

@app.route('/donations_made')
def donations_made():
    # Fetch all users
    users = User.query.all()

    return render_template('donations_made.html', users=users, get_donation_records=get_donation_records)


class BloodRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    request_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)




@app.route('/patient_dashboard')
def patient_dashboard():
    patient_id = session.get('user_id')
    if patient_id:
        patient = Patient.query.get(patient_id)
        blood_requests = BloodRequest.query.filter_by(patient_id=patient_id).all()
        return render_template('patient_dashboard.html', patient=patient, blood_requests=blood_requests)
    else:
        flash('You need to log in as a patient.', 'danger')
        return redirect(url_for('loginpatient'))

@app.route('/make_request', methods=['POST'])
def make_request():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        blood_group = request.form.get('blood_group')
        quantity = request.form.get('quantity')

        if patient_id and blood_group and quantity:
            # Check if the blood inventory has enough quantity
            blood_inventory = BloodInventory.query.filter_by(blood_group=blood_group).first()
            if blood_inventory and blood_inventory.quantity >= int(quantity):
                # Create a new blood request
                new_request = BloodRequest(patient_id=patient_id, blood_group=blood_group, quantity=quantity)
                db.session.add(new_request)
                db.session.commit()

                # Update the blood inventory
                blood_inventory.quantity -= int(quantity)
                db.session.commit()

                flash('Blood request successfully made!', 'success')
                return redirect(url_for('patient_dashboard'))

            flash('Insufficient blood quantity in the inventory.', 'danger')
            return redirect(url_for('patient_dashboard'))

        flash('Invalid blood request data. Please try again.', 'danger')
        return redirect(url_for('patient_dashboard'))



def get_request_records(patient_id):
    return BloodRequest.query.filter_by(patient_id=patient_id).all()

# Route for Blood Request History
@app.route('/blood_request_history')
def blood_request_history():
    # Retrieve all patients
    patients = Patient.query.all()
 
    return render_template('blood_request_history.html', patients=patients,get_request_records=get_request_records)


@app.route('/blood_request_history/<int:patient_id>')
def blood_request_history_for_patient(patient_id):
    # Retrieve the specific patient
    patient = Patient.query.get_or_404(patient_id)

    # Get Blood Request Records for the patient
    request_records = get_request_records(patient.id)

    return render_template('blood_request_history.html', patient=patient, request_records=request_records)

if __name__ == '__main__':
    app.run(debug=True)





if __name__ == '__main__':
    app.run(debug=True)
