from . import admin_blu

@admin_blu.route("/index")
def a_index():
    return "admin"