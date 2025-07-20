import sys
from flask import Flask, request, jsonify, render_template_string
from flasgger import Swagger
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from time import gmtime, strftime
from werkzeug.utils import secure_filename
import os
import base64
import json
import hashlib

"""
INITIALISATION FLASK
"""
RASPBERRY_KEY = sys.argv[1]
app = Flask(
    __name__, static_url_path="", static_folder="static", template_folder="templates"
)
swagger = Swagger(app)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["UPLOADED_FILES"] = ""

"""
INITIALISATION MYSQL
"""

app.config["MYSQL_HOST"] = sys.argv[3]
app.config["MYSQL_USER"] = sys.argv[5]
app.config["MYSQL_PASSWORD"] = sys.argv[4]
app.config["MYSQL_DB"] = sys.argv[2]

mysql = MySQL(app)

"""
API ROUTES FOR CLIENT
"""


@app.route("/client/connect", methods=["POST"])
@cross_origin()
def connect():
    key = request.data
    key = json.loads(key)
    is_connected = False
    try:
        mail = key["email"]
        password = key["password"]
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT password FROM CITY " "WHERE mail = %s", (mail,))
            password_verif = cursor.fetchall()[0][0]
            password = hashlib.sha512(password).hexdigest()
            if password_verif == password:
                is_connected = True
            cursor.close()
    except NameError:
        print("error connection : {}".format(NameError))
    return jsonify({"response": is_connected})


@app.route("/client/get_name", methods=["POST", "GET"])
@cross_origin()
def get_name():
    """
    Get name of city
    ---
    responses:
        200:
            description: List of city
    """
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name FROM CITY")
        list_name = cursor.fetchall()
        cursor.close()
    return jsonify({"name": list_name})


@app.route("/client/get_flag", methods=["POST"])
@cross_origin()
def get_flag():
    """
    Get flag color
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"flag": color_flag}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT color_flag FROM CITY WHERE name = %s", (city,))
        color_flag = cursor.fetchall()[0][0]
        cursor.close()
    return jsonify({"flag": color_flag})


@app.route("/client/get_nb_alert", methods=["POST"])
@cross_origin()
def get_nb_alert():
    """
    Get nb alert
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"red": 0, "orange": 0, "green": 0}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT COLOR FROM WARNINGS WHERE CITY = %s", (city,))
        warnings = cursor.fetchall()
        dico = {"red": 0, "orange": 0, "green": 0}
        for i in range(len(warnings)):
            match warnings[i][0]:
                case 0:
                    dico["red"] += 1
                case 1:
                    dico["orange"] += 1
                case 2:
                    dico["green"] += 1
        cursor.close()
    return jsonify(dico)


@app.route("/client/get_nb_person", methods=["POST"])
@cross_origin()
def get_nb_personne():
    """
    Get nb person
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"beach": response, "sea": response}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT number_beach, number_sea FROM CITY " "WHERE NAME = %s ", (city,)
        )
        response = cursor.fetchall()
        cursor.close()
    return jsonify({"beach": response[0][0], "sea": response[0][1]})


@app.route("/client/get_data_list", methods=["POST"])
@cross_origin()
def get_data_list():
    """
    Get data list
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"data_person_per_hour_on_beach": [],
                "data_person_per_hour_on_sea": [],
                "visibility_sea": [],
                "weather_temperature_beach": [],
                "weather_wind": [],
                "weather_visibility": [],
                "cloud_cover": [],
                }
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        dico = {
            "data_person_per_hour_on_beach": [],
            "data_person_per_hour_on_sea": [],
            "visibility_sea": [],
            "weather_temperature_beach": [],
            "weather_wind": [],
            "weather_visibility": [],
            "cloud_cover": [],
        }
        cursor.execute(
            "SELECT nb_beach,nb_sea,cam_visibility,"
            "temp_beach,wind,visibility,cloud_cover FROM DATA"
            " WHERE CITY = %s ORDER BY ID DESC LIMIT 9 ",
            (city,),
        )
        all_data = cursor.fetchall()
        cursor.close()
    for i in range(len(all_data)):
        j = 0
        for key, value in dico.items():
            value.append(all_data[i][j])
            j += 1
    return jsonify(dico)


@app.route("/client/get_data_alert", methods=["POST"])
@cross_origin()
def get_data_alert():
    """
    Get data alert
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"data": all_data}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT color, information, picture, notif "
            "FROM WARNINGS WHERE CITY = %s "
            "ORDER BY color ASC",
            (city,),
        )
        all_data = cursor.fetchall()
        cursor.close()
    return jsonify({"data": all_data})


@app.route("/client/set_notif", methods=["POST"])
@cross_origin()
def set_notif():
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE WARNINGS SET notif = 1 " "WHERE CITY = %s", (city,))
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/client/get_init_position", methods=["POST"])
@cross_origin()
def get_init_position():
    """
    Get init position
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"latitude": data, "longitude": data}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT latitude, longitude " "FROM city WHERE NAME = %s", (city,)
        )
        data = cursor.fetchall()
    cursor.close()
    return jsonify({"latitude": data[0][0], "longitude": data[0][1]})


@app.route("/client/get_all_position", methods=["POST"])
@cross_origin()
def get_all_position():
    """
    Get all position
    ---
    responses:
        200:
            description: {"data": all_data}
    """
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT latitude, longitude, NAME, "
            "(SELECT COUNT(ID) FROM WARNINGS "
            "WHERE CITY = CITY.NAME) "
            "FROM CITY"
        )
        all_data = cursor.fetchall()
        cursor.close()
    return jsonify({"data": all_data})


@app.route("/client/get_picture", methods=["POST"])
@cross_origin()
def get_picture_base_64():
    """
    Get picture base 64
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"picture": base64_data}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    city = city.replace(" ", "_")
    with open(app.config["UPLOADED_FILES"] + city, "rb") as image_file:
        image_data = image_file.read()
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return jsonify({"picture": base64_data})


"""
API ROUTES FOR RASPBERRY
"""


@app.route("/machine/set_flag", methods=["POST"])
@cross_origin()
def set_flag():
    """
    set flag
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
        - name: color
          in: path
          type: number
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    color = key["color"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE CITY SET color_flag= %s " "WHERE NAME = %s", (color, city)
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/machine/set_number_people", methods=["POST"])
@cross_origin()
def set_number_people():
    """
    set number peale
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
        - name: nb_beach
          in: path
          type: number
          required: true
        - name: nb_sea
          in: path
          type: number
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    nb_beach = key["nb_beach"]
    nb_sea = key["nb_sea"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE CITY SET number_beach= %s, " "number_sea= %s" "WHERE NAME = %s",
            (nb_beach, nb_sea, city),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/machine/delete_alert_by_city", methods=["POST"])
@cross_origin()
def delete_alert_by_id():
    """
    delete alert
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM WARNINGS WHERE city = %s", (city,))
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/machine/add_alert", methods=["POST"])
@cross_origin()
def add_alert():
    """
    add alert
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
        - name: color
          in: path
          type: number
          required: true
        - name: message
          in: path
          type: string
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    color = key["color"]
    message = key["message"]
    city = key["city"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT MAX(ID) FROM WARNINGS")
        id_alert = cursor.fetchall()[0][0] + 1
        cursor.execute(
            "INSERT INTO WARNINGS(ID,color,information,city,notif)"
            "VALUES(%s,%s,%s,%s,%s)",
            (id_alert, color, message, city, 0),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"id": id_alert})


@app.route("/machine/add_data_city", methods=["POST"])
@cross_origin()
def add_data_city():
    """
    add data city
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
        - name: nb_beach
          in: path
          type: number
          required: true
        - name: nb_sea
          in: path
          type: number
          required: true
        - name: precipitation
          in: path
          type: number
          required: true
        - name: temp_beach
          in: path
          type: number
          required: true
        - name: cloud_cover
          in: path
          type: number
          required: true
        - name: wind
          in: path
          type: number
          required: true
        - name: visibility
          in: path
          type: number
          required: true
        - name: cam_visibility
          in: path
          type: number
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    nb_beach = key["nb_beach"]
    nb_sea = key["nb_sea"]
    precipitation = key["precipitation"]
    temp_beach = key["temp_beach"]
    cloud_cover = key["cloud_cover"]
    wind = key["wind"]
    visibility = key["visibility"]
    cam_visibility = key["cam_visibility"]
    time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT MAX(ID) FROM DATA")
        id_data = cursor.fetchall()[0][0] + 1
        cursor.execute(
            "INSERT INTO DATA(ID,CITY,nb_beach,nb_sea,"
            "time,precipitation,temp_beach,cloud_cover,wind,"
            "visibility,cam_visibility)"
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                id_data,
                city,
                nb_beach,
                nb_sea,
                time,
                precipitation,
                temp_beach,
                cloud_cover,
                wind,
                visibility,
                cam_visibility,
            ),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/machine/add_picture_alert_or_moment", methods=["POST"])
@cross_origin()
def add_picture_alert_or_moment():
    """
    add picture
    ---
    parameters:
        - name: key
          in: path
          type: string
          required: true
        - name: file
          in: path
          type: file
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    # key = request.data
    # key = json.loads(key)
    # key = key["key"]
    # if key != RASPBERRY_KEY:
    #    return jsonify({"res": "key error"})
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOADED_FILES"], filename))
    return jsonify({"res": "yes"})


@app.route("/machine/new_site", methods=["POST"])
@cross_origin()
def add_city():
    key = request.data
    key = json.loads(key)
    name = key["name"]
    mail = key["mail"]
    password = key["password"]
    latitude = key["latitude"]
    longitude = key["longitude"]
    color_flag = key["color_flag"]
    actual_picture = key["actual_picture"]
    number_beach = key["number_beach"]
    number_sea = key["number_sea"]
    key_api = key["key"]
    if key_api != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO CITY(NAME,mail"
            ",password,latitude,longitude"
            ",color_flag,actual_picture,"
            "number_beach,number_sea)"
            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                name,
                mail,
                password,
                latitude,
                longitude,
                color_flag,
                actual_picture,
                number_beach,
                number_sea,
            ),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


"""
SUPERVISION
"""


@app.route("/supervision/all_pictures", methods=["GET"])
@cross_origin()
def display_all_picture():
    key = request.args.get("key")
    if key != RASPBERRY_KEY:
        return jsonify({"error": "Access denied"})
    html: str = ""
    for filename in os.listdir("."):
        if filename.endswith(".png"):
            image = open(filename, "rb")
            encoded_string = base64.b64encode(image.read())
            encoded_string = encoded_string.decode("utf-8")
            html += (
                f"<img src='data:image/png;base64,{encoded_string}' "
                f"width='500' height='500' /><h2>{filename}</h2>"
            )
    return render_template_string(html)


"""
ZONE
"""


@app.route("/zone", methods=["GET"])
@cross_origin()
def get_zone():
    """
    Get zone
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"data": all_data}
    """
    city = request.args.get("city")
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT ID,type,x1,x2,y1,y2 " "FROM line WHERE ville=%s",
            (city,),
        )
        all_data = cursor.fetchall()
        cursor.close()
    return jsonify({"data": all_data})


@app.route("/zone", methods=["POST"])
@cross_origin()
def add_zone():
    """
    Add zone
    ---
    parameters:
        - name: city
          in: path
          type: string
          required: true
        - name: type
          in: path
          type: number
          required: true
        - name: x1
          in: path
          type: number
          required: true
        - name: x2
          in: path
          type: number
          required: true
        - name: y1
          in: path
          type: number
          required: true
        - name: y2
          in: path
          type: number
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    city = key["city"]
    type = key["type"]
    x1 = key["x1"]
    x2 = key["x2"]
    y1 = key["y1"]
    y2 = key["y2"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO line(ville,type,x1,x2,y1,y2) " "VALUES(%s,%s,%s,%s,%s,%s)",
            (city, type, x1, x2, y1, y2),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/zone", methods=["DELETE"])
@cross_origin()
def delete_zone():
    """
    Delete zone
    ---
    parameters:
        - name: id
          in: path
          type: number
          required: true
        - name: key
          in: path
          type: string
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    id = key["id"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM line WHERE id=%s",
            (id,),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/zone", methods=["PUT"])
@cross_origin()
def update_line_param():
    """
    Update zone
    ---
    parameters:
        - name: id
          in: path
          type: number
          required: true
        - name: key
          in: path
          type: string
          required: true
        - name: x1
          in: path
          type: number
          required: true
        - name: x2
          in: path
          type: number
          required: true
        - name: y1
          in: path
          type: number
          required: true
        - name: y2
          in: path
          type: number
          required: true
    responses:
        200:
            description: {"res": "yes"}
    """
    key = request.data
    key = json.loads(key)
    id = key["id"]
    x1 = key["x1"]
    x2 = key["x2"]
    y1 = key["y1"]
    y2 = key["y2"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE line SET x1=%s,x2=%s,y1=%s,y2=%s " "WHERE id=%s",
            (x1, x2, y1, y2, id),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


@app.route("/machine/city", methods=["GET"])
@cross_origin()
def get_city():
    """
    Get city details
    ---
    parameters:
        - name: detector_id
          in: query
          type: integer
          required: true
    responses:
        200:
            description: {"data": city_data}
    """
    detector_id = request.args.get("detector_id", type=int)
    if detector_id is None:
        return jsonify({"error": "detector_id is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT NAME, "
        "latitude, "
        "longitude, "
        "ip, "
        "name_ip, "
        "password_ip, "
        "blur, "
        "run_detection, "
        "type_detection, "
        "launch_detection, "
        "stop_detection, "
        "public_url "
        "FROM CITY "
        "WHERE detector_id = %s",
        (detector_id,),
    )
    city_data = cursor.fetchall()
    cursor.close()
    return jsonify({"data": city_data})


@app.route("/machine/cache_size", methods=["GET"])
@cross_origin()
def get_cache_size():
    """
    Get cache size
    ---
    parameters:
        - name: detector_id
          in: query
          type: integer
          required: true
    responses:
        200:
            description: {"cache_size": cache_size}
    """
    detector_id = request.args.get("detector_id", type=int)
    if detector_id is None:
        return jsonify({"error": "detector_id is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT cache_size FROM CITY WHERE detector_id = %s", (detector_id,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return jsonify({"cache_size": result[0]})
    return jsonify({"cache_size": 4})


@app.route("/machine/zone_orange", methods=["GET"])
@cross_origin()
def get_zone_orange():
    """
    Get orange zone coordinates
    ---
    parameters:
        - name: city
          in: query
          type: string
          required: true
    responses:
        200:
            description: {"data": result}
    """
    city = request.args.get("city")
    if city is None:
        return jsonify({"error": "city is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT x1, x2, y1, y2 FROM line WHERE ville = %s AND type = 1", (city,)
    )
    result = cursor.fetchall()
    cursor.close()
    return jsonify({"data": result})


@app.route("/machine/zone_red", methods=["GET"])
@cross_origin()
def get_zone_red():
    """
    Get red zone coordinates
    ---
    parameters:
        - name: city
          in: query
          type: string
          required: true
    responses:
        200:
            description: {"data": result}
    """
    city = request.args.get("city")
    if city is None:
        return jsonify({"error": "city is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT x1, x2, y1, y2 FROM line WHERE ville = %s AND type = 2", (city,)
    )
    result = cursor.fetchall()
    cursor.close()
    return jsonify({"data": result})


@app.route("/machine/zone_green", methods=["GET"])
@cross_origin()
def get_zone_green():
    """
    Get green zone coordinates
    ---
    parameters:
        - name: city
          in: query
          type: string
          required: true
    responses:
        200:
            description: {"data": result}
    """
    city = request.args.get("city")
    if city is None:
        return jsonify({"error": "city is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT x1, x2, y1, y2 FROM line WHERE ville = %s AND type = 0", (city,)
    )
    result = cursor.fetchall()
    cursor.close()
    return jsonify({"data": result})


@app.route("/machine/zone", methods=["GET"])
@cross_origin()
def get_all_zone():
    """
    Get green zone coordinates
    ---
    parameters:
        - name: city
          in: query
          type: string
          required: true
    responses:
        200:
            description: {"data": result}
    """
    city = request.args.get("city")
    if city is None:
        return jsonify({"error": "city is required"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, x1, x2, y1, y2, algo,type,filter_size,threshold_luminosity FROM line WHERE ville = %s",
        (city,),
    )
    result = cursor.fetchall()
    cursor.close()
    return jsonify({"data": result})


@app.route("/machine/post_measuring_data", methods=["POST"])
@cross_origin()
def post_measuring_zone_data():
    key = request.data
    key = json.loads(key)
    zone_id = key["zone_id"]
    counting_data = key["counting_data"]
    time = key["time"]
    key = key["key"]
    if key != RASPBERRY_KEY:
        return jsonify({"res": "key error"})
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO measuring_data (zone_id, counting_data, time) "
            "VALUES (%s, %s, %s)",
            (zone_id, counting_data, time),
        )
        mysql.connection.commit()
        cursor.close()
    return jsonify({"res": "yes"})


"""
LAUNCH APPLICATION
"""

app.run(host="0.0.0.0", port=5000)
