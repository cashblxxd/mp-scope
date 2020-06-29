from flask import *
from mongo import user_exist, username_taken, put_confirmation_token, get_confirmation_token, user_create,\
    get_session, init_session, modify_session, delete_session, get_items, get_postings, insert_postings_update_job, \
    insert_items_update_job, insert_act_job, get_items_ids, get_postings_ids
from mailer import send_join_mail
from pprint import pprint
from time import sleep
import secrets


app = Flask(__name__)
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"


def check():
    global mongosession
    if "uid" not in session:
        session["uid"] = secrets.token_urlsafe()
        return redirect("/login")
    mongosession = get_session(session["uid"])
    if mongosession is None or len(mongosession["order"]) == 0:
        return redirect("/login")


@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    :param
    active: ["dashboard", "dynamics", "sales", "analysis", "mp_purchases", "losses", "map", "traffic", "competitiors", "facilities", "settings"]
    :return:
    """
    check()
    pprint(mongosession)
    cur_pos, active = request.args.get("u", "-no-such-"), request.args.get("page", "-no-such-")
    updating, getting = request.args.get("updating", "none"), request.args.get("getting", "none")
    if cur_pos == "-no-such-" and "cur_pos" not in mongosession:
        mongosession["cur_pos"] = 1
    if active == "-no-such-" and "active" not in mongosession:
        mongosession["active"] = "dashboard"
    if cur_pos != "-no-such-" and str(cur_pos).isdigit() and int(cur_pos) <= len(mongosession["order"]):
        mongosession["cur_pos"] = int(cur_pos)
    if active != "-no-such-" and active in {"dashboard", "dynamics", "sales", "analysis", "mp_purchases", "losses",
                                            "map", "traffic", "competitiors", "facilities", "settings"}:
        mongosession["active"] = active
    data = "Нет данных для отображения"
    if mongosession["active"] == "dashboard":
        tab = request.args.get("tab", "-no-such-")
        if tab == "-no-such-" and "tab" not in mongosession:
            mongosession["tab"] = "visible"
        if tab != "-no-such-" and tab in {"items_all", "processing", "moderating", "processed", "failed_moderation",
                                          "failed_validation", "failed", "all", "awaiting_packaging",
                                          "awaiting_deliver", "arbitration", "delivering", "delivered", "cancelled"}:
            mongosession["tab"] = tab
            '''
            "visible", "invisible", "ready_to_supply", "state_failed"
            '''
        print(mongosession["tab"])
        if mongosession["tab"] in {"items_all", "processing", "moderating", "processed", "failed_moderation",
                                   "failed_validation", "failed"}:
            print(1)

            user = mongosession["users"][mongosession["order"][mongosession["cur_pos"] - 1]]
            data = get_items(user["ozon_apikey"], user["client_id"])
            if data is None:
                data = "Нет данных для отображения"
            else:
                data = data["data"]
            pprint(data)
            if mongosession["tab"] != "items_all":
                ids = get_items_ids(user["ozon_apikey"], user["client_id"], mongosession["tab"])
                data_new = {}
                for i in ids:
                    data_new[i] = data[i]
                data = data_new
                if not data:
                    data = "Нет данных для отображения"
        elif mongosession["tab"] in {"all", "awaiting_packaging", "awaiting_deliver", "arbitration",
                                     "delivering", "delivered", "cancelled"}:
            user = mongosession["users"][mongosession["order"][mongosession["cur_pos"] - 1]]
            data = get_postings(user["ozon_apikey"], user["client_id"])
            if data is None:
                data = "Нет данных для отображения"
            else:
                data = data["data"]
            if mongosession["tab"] != "all":
                ids = get_postings_ids(user["ozon_apikey"], user["client_id"], mongosession["tab"])
                data_new = {}
                for i in ids:
                    data_new[i] = data[i]
                data = data_new
                if not data:
                    data = "Нет данных для отображения"
    print(mongosession)
    modify_session(session["uid"], mongosession)
    pprint(mongosession)
    return render_template("accounts-12.html", data=data, accounts=mongosession["order"], cur_pos=mongosession["cur_pos"], active=mongosession["active"], tab=mongosession["tab"], updating=updating, getting=getting)


@app.route('/update', methods=['GET', 'POST'])
def update():
    check()
    q, u = request.args.get("q", "none"), request.args.get("u", "none")
    if q not in ["items", "postings"]:
        return redirect("/dashboard")
    if not u.isdigit():
        u = mongosession["cur_pos"]
    user = mongosession["users"][mongosession["order"][int(u) - 1]]
    if q == "items":
        insert_items_update_job(user["ozon_apikey"], user["client_id"], f'items_update:{user["ozon_apikey"]}:{user["client_id"]}')
        return redirect(f"/dashboard?updating={q}")
    if q == "postings":
        insert_postings_update_job(user["ozon_apikey"], user["client_id"], f'items_update:{user["ozon_apikey"]}:{user["client_id"]}')
        return redirect("/dashboard?updating=postings")


@app.route('/get_act', methods=['GET', 'POST'])
def get_act():
    check()
    u = request.args.get("u", "none")
    if not u.isdigit():
        u = mongosession["cur_pos"]
    user = mongosession["users"][mongosession["order"][int(u) - 1]]
    insert_act_job(user["ozon_apikey"], user["client_id"], f'get_act:{user["ozon_apikey"]}:{user["client_id"]}')
    return redirect("/dashboard?getting=act")


@app.route('/confirm', methods=['GET', 'POST'])
def confirm_join():
    token = request.args.get("token", "")
    if token:
        response, message = get_confirmation_token(token)
        print(response, message)
        if response:
            username, password = message
            response, data = user_create(username, password)
            if response:
                if "uid" not in session:
                    session["uid"] = secrets.token_urlsafe()
                mongosession = get_session(session["uid"])
                if mongosession is None:
                    init_session(session["uid"])
                    mongosession = get_session(session["uid"])
                mongosession["users"][username] = data
                mongosession["order"] = mongosession.get("order", []) + [username]
                modify_session(session["uid"], mongosession)
                return redirect("/")
    return render_template("login.html")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    delete_session(session.get("uid", "-"))
    session.pop("uid", None)
    return redirect("/login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("got it")
        username, password = request.form.get("username", ""), request.form.get("password", "")
        print(username, password)
        if username and password:
            print("there")
            response = user_exist(username, password)
            if response[0]:
                data = response[1]
                if "uid" not in session:
                    session["uid"] = secrets.token_urlsafe()
                mongosession = get_session(session["uid"])
                if mongosession is None:
                    init_session(session["uid"])
                    mongosession = get_session(session["uid"])
                mongosession["users"][username] = data
                mongosession["order"] = mongosession.get("order", []) + [username]
                modify_session(session["uid"], mongosession)
                return redirect("/")
            else:
                print("nope")
                return render_template("login.html", attempt=True)
        return redirect("/")
    return render_template("login.html")


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        print("got it register")
        email, password = request.form.get("email", ""), request.form.get("password", "")
        print(email, password)
        if email and password:
            print("lol rly")
            if not username_taken(email):
                print("rendering success")
                token = put_confirmation_token(email, password)
                send_join_mail(email, token)
                return render_template("join_success.html")
            else:
                print("oops")
                return render_template("registration.html", attempt=True)
    return render_template("registration.html")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', threaded=True)
    app.app_context().push()
