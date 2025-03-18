from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import time
import x
import os
import uuid
from icecream import ic

ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

##############################
@app.after_request
def disable_cache(response):
    """
    This function automatically disables caching for all responses.
    It is applied after every request to the server.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

#############################
@app.get("/send-email")
def send_email():
    try:
        x.send_email()
        return "email"
    except Exception as ex:
        ic(ex)
        return "error"



##############################
@app.get("/")
def show_index():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM items ORDER BY item_pk LIMIT %s OFFSET %s"
        cursor.execute(q, (2, 0))
        rows = cursor.fetchall()
        ic(rows)
        is_session = False
        if session.get("user"): is_session = True
        active_index = "active"
        return render_template("page_index.html", title="Shelters Home Page", is_session = is_session, active_index=active_index, rows=rows)
    except Exception as ex:
        return "System under maintainance", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/profile")
def show_profile():
    active_profile ="active"
    error_message = request.args.get("error_message", "")
    try:
        is_session = False
        if session["user"]: is_session = True
        return render_template("page_profile.html", title="Profile", user=session["user"], x=x, is_session=is_session, active_profile=active_profile, 
                           error_message=error_message,
                           old_values={})
    except Exception as ex:
        ic(ex)
        return redirect(url_for("show_login"))


##############################
@app.get("/signup")
def show_signup():
    active_signup ="active"
    error_message = request.args.get("error_message", "")
    try:
        return render_template("page_signup.html", title="Shelter Signup", x=x, active_signup=active_signup, 
                           error_message=error_message,
                           old_values={})
    except Exception as ex:
        ic(ex)
    finally:
       pass

##############################
@app.post("/signup")
def signup():
    try:
        user_name = x.validate_user_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        hashed_password = generate_password_hash(user_password)
        verification_key = str(uuid.uuid4())
        # ic(hashed_password)
        user_created_at = int(time.time())

        q = """INSERT INTO users
        (user_pk, user_name, user_last_name, user_email,
         user_password, user_created_at, user_updated_at,
         user_deleted_at,
         user_verified_at, user_verification_key)
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, 0, %s)"""

        db, cursor = x.db()
        cursor.execute(q, (
            user_name, 
            user_last_name, 
            user_email, 
            hashed_password,
            user_created_at, 
            0, 
            0, 
            verification_key
              ))
        if cursor.rowcount != 1: 
            raise Exception("System under maintenance")
        
        db.commit()

        x.send_email(user_name, user_email, verification_key)
        return redirect(url_for("show_login", message="Signup ok"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        old_values = request.form.to_dict()

        if "username" in str(ex):
            old_values.pop("user_user_name", None)
            return render_template("signup.html",                                   
                error_message="Invalid username", old_values=old_values, user_user_name_error="input_error")
        if "first name" in str(ex):
            old_values.pop("user_name", None)
            return render_template("signup.html",
                error_message="Invalid name", old_values=old_values, user_name_error="input_error")
        if "last name" in str(ex):
            old_values.pop("user_last_name", None)
            return render_template("signup.html",
                error_message="Invalid last name", old_values=old_values, user_last_name_error="input_error")
        if "Invalid email" in str(ex):
            old_values.pop("user_email", None)
            return render_template("signup.html",
                error_message="Invalid email", old_values=old_values, user_email_error="input_error")
        if "password" in str(ex):
            old_values.pop("user_password", None)
            return render_template("signup.html",
                error_message="Invalid password", old_values=old_values, user_password_error="input_error")

        if "users.user_email" in str(ex):
            return redirect(url_for("show_signup",
                error_message="Email already exists", old_values=old_values, email_error=True))
        if "users.user_user_name" in str(ex): 
            return redirect(url_for("show_signup", 
                error_message="Username already exists", old_values=old_values, user_user_name_error=True))
        return redirect(url_for("show_signup", error_message=ex.args[0]))

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close() 



#############################
@app.get("/verify/<verification_key>")
def verify(verification_key):
    try:
        db, cursor = x.db()
 
        q = "SELECT user_pk FROM users WHERE user_verification_key = %s AND user_verified_at = 0"
        cursor.execute(q, (verification_key,))
        user = cursor.fetchone()
 
        if not user:
            return "Invalid or already used verification key."
        current_time = int(time.time())
        q_update = """UPDATE users
                      SET user_verified_at = %s,
                        user_verification_key = NULL
                      WHERE user_pk = %s"""
        cursor.execute(q_update, (current_time, user["user_pk"]))
        db.commit()
        return "Your account has been verified!"
    except Exception as ex:
        ic(ex)
        if "db" in locals():
            db.rollback()
        return "Verification failed", 500
    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()



##############################
@app.get("/login")
def show_login():
    active_login = "active"
    message = request.args.get("message", "")
    try:
        return render_template("page_login.html", title="Shelter Login", x=x, active_login = active_login,  message = message, old_values={})
    except Exception as ex:
        ic(ex)
    finally:
       pass


##############################
@app.post("/login")
def login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone() 
        ic(user)
        if not user: raise Exception("User not found")
        if user["user_verified_at"] == 0: raise Exception("User not verified")
        if not check_password_hash(user["user_password"], user_password):
            raise Exception("Invalid credentials")
        user.pop("user_password")
        session["user"] = user  
        return redirect(url_for("show_profile"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        old_values = request.form.to_dict()

        if "Invalid email" in str(ex):
            old_values.pop("user_email", None)
            return render_template("page_login.html",
                message="Invalid email", old_values=old_values)
        
        if "password" in str(ex):
            old_values.pop("user_password", None)
            return render_template("page_login.html",
                message="Invalid password", old_values=old_values)
        return redirect(url_for("show_login", message=ex.args[0]))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("show_login"))


##############################
@app.get("/items/page/<page_number>")
def get_items_by_page(page_number):
    try:
        # Validate - make sure that the page number is a digit/number
        page_number = x.validate_page_number(page_number)
        next_page = page_number + 1  
        limit = 2
        temp_limit = limit + 1 
        offset = (int(page_number) - 1) * limit
        db, cursor = x.db()
        q = "SELECT * FROM items ORDER BY item_pk LIMIT %s OFFSET %s"
        cursor.execute(q, (temp_limit, offset))
        rows = cursor.fetchall()
        ic(len(rows))
        if(len(rows)) < 3:
            button_html = """<mixhtml mix-remove="#button_get_more_items"></mixhtml>"""
        else:
            button = render_template("_button_get_more_items.html", next_page=next_page)
            button_html = f"""
                <mixhtml mix-update="#button_get_more_items">
                    {button}
                </mixhtml>
            """
            # button_get_more_items = render_template("_button_get_more_items.html", next_page=next_page)
            
        final_html = ""
        for row in rows[:2]:
            item_html = render_template("_item.html", row=row)
            final_html += item_html
        return f"""
            <mixhtml mix-bottom="#items">
                {final_html}
            </mixhtml>
            { button_html }
        """
    except Exception as ex:
        ic(ex)
        if "page number not valid" in str(ex): return "wrong page", 400
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()




#################################

app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.post("/add-item")
def add_item():
    try:
        item_pk = str(uuid.uuid4())
        item_name = x.validate_item_name()
        item_address = x.validate_item_address()
        item_lat = x.validate_item_lat()
        item_lon = x.validate_item_lon()
        item_image = x.validate_item_image()
        
        image_filename = None
        if item_image:
            image_filename = secure_filename(item_image.filename)
            upload_dir = os.path.join("static", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            item_image.save(os.path.join(upload_dir, image_filename))
        
        db, cursor = x.db()
        q = """INSERT INTO items
               (item_pk, item_name, item_address, item_lat, item_lon, item_image)
               VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(q, (
            item_pk, 
            item_name, 
            item_address, 
            item_lat, 
            item_lon, 
            image_filename
            ))
        if cursor.rowcount != 1:
            raise Exception("Could not insert item")

        db.commit()

        return redirect(url_for("show_index"))
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        old_values = request.form.to_dict()
        
        if "Shelter name" in str(ex):
            old_values.pop("item_name", None)
            return render_template("add-item.html", error_message="input_error")
        
        if "Address" in str(ex):
            old_values.pop("item_address", None)
            return render_template("add-item.html", error_message="input_error")
        
        if "latitude" in str(ex):
            old_values.pop("item_lat", None)
            return render_template("add-item.html", error_message="input_error")
        
        if "latitude" in str(ex):
            old_values.pop("item_longitude", None)
            return render_template("add-item.html", error_message="input_error")
        
        return redirect(url_for("show_profile", error_message=str(ex)))
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()