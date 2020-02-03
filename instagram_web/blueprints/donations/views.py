from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from models.donation import Donation
from flask_login import current_user
import braintree
import os
from instagram_web.util.email_helper import donation_email

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv('BRAINTREE_MERCHANT_ID'),
        public_key=os.getenv('BRAINTREE_PUBLIC_KEY'),
        private_key=os.getenv('BRAINTREE_PRIVATE_KEY')
    )
)


donations_blueprint = Blueprint('donations', 
                                __name__,
                                template_folder='templates')

@donations_blueprint.route('/new/<id>', methods=['GET'])
def new(id):
    image = Image.get_by_id(id)
    token = gateway.client_token.generate()
    return render_template('donations/new.html', token=token, image=image)

@donations_blueprint.route('/<id>', methods=['POST'])
def create(id):
    amount = float(request.form['amount'])
    result = gateway.transaction.sale({
        "amount": ("%.2f" % amount ),
        "payment_method_nonce": request.form['payment_method_nonce'],
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        print(result)
        donate = Donation(donor=current_user.id,image=id,amount=result.transaction.amount)
        if donate.save():
            # receiver = Image.get_by_id(id).user_id
            # receiver = User.select().join(Image).where(Image.id == id)
            receiver = User.get_by_id(Image.get_by_id(id).user_id)
            donation_email(receiver,result.transaction.amount)
            # breakpoint()
            flash("Payment successfully made!","alert alert-success")
            return redirect(url_for('users.show',username=current_user.username))
        else:
            flash("Something went wrong. Try again later.","alert alert-danger")
            render_template("users/show.html",username=current_user.username)
    else:
        for x in result.errors.deep_errors: 
            flash(f'Error- {x.code}: {x.message}' ,"alert alert-danger")
        return redirect(url_for('users.show',username=current_user.username))
