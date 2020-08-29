from flask import Flask,request,redirect,render_template,url_for,send_from_directory
from markupsafe import escape
import calculator as hsc

application = Flask(__name__)

@application.route('/')
def index():
    return redirect(url_for('calculation'))


@application.route('/calculation', methods=["POST", "GET"])
def calculation():
    if request.method == "POST":
        winning_needed = round(float(request.form["total_winning_needed"]))
        winning_star_bounce = round(float(request.form["winning_star_bounce"]))
        rate = float(request.form["winning_rate"])
        five_to_one = request.form["five_to_one"] == "Yes"

        imd = hsc.run(
            total_winning_needed=winning_needed,
            star_bounce=winning_star_bounce,
            winning_rate=rate,
            have_five_to_one=five_to_one
        )
        
        # file_url = url_for('download_file', filename=str(file_id) + '.png')
        return render_template('result.html',file_url=imd)
    else:
        return render_template('calculation.html')


@application.route('/download_file/<filename>')
def download_file(filename):
    return send_from_directory('templates\pic',
                               filename, as_attachment=True)


if __name__ == "__main__":
    application.run()



