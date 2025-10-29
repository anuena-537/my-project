from flask import Flask, render_template, request, redirect, url_for
import pywhatkit

app = Flask(__name__)

patients = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        patient_name = request.form["patient_name"]
        patients[patient_name] = {"medicines": [], "phone_number": ""}
        return redirect(url_for("add_patient_details", patient_name=patient_name))
    return render_template("index.html", patients=patients)

@app.route("/add_patient_details/<patient_name>", methods=["GET", "POST"])
def add_patient_details(patient_name):
    if request.method == "POST":
        phone_number = request.form["phone_number"]
        patients[patient_name]["phone_number"] = phone_number
        return redirect(url_for("add_medicine", patient_name=patient_name))
    return render_template("add_patient_details.html", patient_name=patient_name)

@app.route("/add_medicine/<patient_name>", methods=["GET", "POST"])
def add_medicine(patient_name):
    if request.method == "POST":
        medicine_name = request.form["medicine_name"]
        time_str = request.form["time"]
        patients[patient_name]["medicines"].append({"name": medicine_name, "time": time_str})
        return redirect(url_for("add_medicine", patient_name=patient_name,time_str=time_str))
    return render_template(
        "add_medicine.html",
        patient_name=patient_name,
        medicines=patients[patient_name]["medicines"]
    )

@app.route("/send_message/<patient_name>/<medicine_name>/<time_str>")
def send_message(patient_name, medicine_name, time_str):
    """Send WhatsApp message instantly but include the entered time in the message."""
    phone_number = patients[patient_name]["phone_number"]
    message = f"💊 Reminder: It's time to take your medicine '{medicine_name}' at {time_str}!"

    try:
        # Send instantly (no scheduling)
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=message,
            wait_time=10,      # small delay to open tab and send
            tab_close=True
        )
        print(f"✅ Message sent instantly to {phone_number}")

    except Exception as e:
        print(f"❌ Error sending message: {e}")

    return redirect(url_for("add_medicine", patient_name=patient_name))

if __name__ == "__main__":
    app.run(debug=True)
