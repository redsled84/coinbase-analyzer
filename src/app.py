from flask import Flask, render_template, url_for
from client import get_account_info, get_crypto_data
app = Flask(__name__)

@app.route('/')
def portfolio(name=None):
	info = get_account_info()

	btc_nums = get_crypto_data('BTC')
	bch_nums = get_crypto_data('BCH')
	eth_nums = get_crypto_data('ETH')
	dash_nums = get_crypto_data('DASH')
	zrx_nums = get_crypto_data('ZRX')
	xrp_nums = get_crypto_data('XRP')
	dnt_nums = get_crypto_data('DNT')
	xlm_nums = get_crypto_data('XLM')
	link_nums = get_crypto_data('LINK')

	return render_template('index.html', info=info,
		btc_nums=btc_nums,
		bch_nums=bch_nums,
		eth_nums=eth_nums,
		dash_nums=dash_nums,
		zrx_nums=zrx_nums,
		xrp_nums=xrp_nums,
		dnt_nums=dnt_nums,
		xlm_nums=xlm_nums,
		link_nums=link_nums)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['pragma'] = 'no-cache'
    return response
