from flask import Blueprint, request, render_template, redirect
from database import get_user_by_token, store_secret_key
import pyotp
import qrcode
import base64
from io import BytesIO

two_factor = Blueprint('two_factor', __name__)

@two_factor.route('/check_2fa', methods=['GET', 'POST'])
def check_2fa():
    if request.method == 'GET' and 'token' in request.cookies:
        token = request.cookies['token']
        user = get_user_by_token(token)
        if user is not None and 'secret_key' in user:
            return render_template('/check_2fa.html')
        else:
            return 'Invalid request', 403

    elif request.method == 'POST':
        secret_key = None
        user = get_user_by_token(request.cookies['token'])
        if user is not None and 'secret_key' in user:
            secret_key = user['secret_key']

        if secret_key is None:
            return 'Invalid request', 403

        code = request.form['code']
        totp = pyotp.TOTP(secret_key)
        is_correct = totp.verify(code)
        if is_correct:
            return redirect('/')

    return 'Invalid request', 403 


@two_factor.route('/setup_2fa', methods=['GET', 'POST'])
def setup_2fa():
    if request.method == 'GET' and 'token' in request.cookies:
        secret_key = pyotp.random_base32()
        user = get_user_by_token(request.cookies['token'])
        username = user['username']

        store_secret_key(username, secret_key)

        qr_code_data = pyotp.totp.TOTP(secret_key).provisioning_uri(
            name=username, 
            issuer_name='Hide My Secret Sauce'
        )

        qr_code = qrcode.make(qr_code_data)
        buffered = BytesIO()
        qr_code.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return render_template('setup_2fa.html', data=img_str)
    elif 'token' not in request.cookies:
        return 'Invalid request', 403
    else:
        user = get_user_by_token(request.cookies['token'])
        if user is None or 'secret_key' not in user:
            return 'Invalid request', 403

        secret_key = user['secret_key']
        code = request.form['code']
        totp = pyotp.TOTP(secret_key)
        is_correct = totp.verify(code, valid_window=2)

        if is_correct:
            return redirect('/')

        return 'incorrect key'

