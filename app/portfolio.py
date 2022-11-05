from flask import (
        Blueprint, render_template, request, redirect, url_for, current_app
)
import sendgrid
from sendgrid.helpers.mail import *

bp = Blueprint("portfolio", __name__, url_prefix='/')

@bp.route('/', methods=["GET"])
def index():
    return render_template("portfolio/index.html")

@bp.route("/mail", methods=["GET", "POST"])
def mail():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        errors = []
        if not email:
            errors.append("Email is required")
        if not subject:
            errors.append("Subject is required")
        if not content:
            errors.append("Content is required")
        
        if len(errors) == 0:
            send_email(name, email, message)
            return render_template("portfolio/sent_mail.html")
        else:
            for error in errors:
                flash(error)

    return redirect(url_for("portfolio.index"))

def send_email(name, email, message):
    my_email = "g2siengrain@gmail.com"
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config["SENDGRID_KEY"])

    from_email = Email(my_email)
    to_email = To(my_email, substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,
    })
    
    html_content = """
        <p>Hi Gon, you have a new message from your web:</p>
        <p>Nombre: -name-</p>
        <p>Email: -email-</p>
        <p>Message: -message-</p>
    """
    mail = Mail(my_email, to_email, "New message from your web", html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())
