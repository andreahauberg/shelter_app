from flask import Flask, render_template
app = Flask(__name__)


########################
@app.route('/')
def show_index():
    return render_template('show_index.html', title="Welcome")


@app.get("/items/page/<page_number>")
def get_items(page_number):
    try:
        # Hardcoded items
        items = [
            {"item_pk": "3", "item_image": "shelter.png", "item_adress": "address 3"},
            {"item_pk": "4", "item_image": "shelter.png", "item_adress": "address 4"},
        ]
        return {"items": items}  # Return items as JSON
    except Exception as ex:
        return {"error": str(ex)}, 500
    

########################
@app.route('/about')
def show_about():
    return render_template('show_about.html', title="About")

########################
@app.route('/contact')
def show_contact():
    return render_template('show_contact.html', title="Contact")