from . import staff_blu

@staff_blu.route("/staff/index")
def s_index():
    return 'staff'