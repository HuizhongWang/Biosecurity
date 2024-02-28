from . import admin_blu

@admin_blu.route("/admin/index")
def a_index():
    return "admin"