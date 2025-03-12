from flask import Flask, render_template
app = Flask(__name__)
import x

from icecream import ic
ic.configureOutput(prefix=f'***** | ', includeContext=True)


##############################
@app.get("/")
def show_index():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM items ORDER BY item_pk LIMIT %s OFFSET %s"
        cursor.execute(q, (2, 0))
        rows = cursor.fetchall()
        ic(rows)
        return render_template("page_index.html", title="Shelters Home Page", rows=rows)
    except Exception as ex:
        ic(ex)
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.get("/signup")
def show_signup():
    try:
        return render_template("page_signup.html", title="Shelter Signup", x=x)
    except Exception as ex:
        ic(ex)
    finally:
       pass


##############################
@app.get("/login")
def show_login():
    try:
        return render_template("page_login.html", title="Shelter Login", x=x)
    except Exception as ex:
        ic(ex)
    finally:
       pass


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




