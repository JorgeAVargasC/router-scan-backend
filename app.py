import bcrypt
import time

from flask import Flask, jsonify, request
from flask import Flask, jsonify
from flask_cors import CORS


# * ============ (Core functions) ============ *#

from utils.save_results_in_db import save_results_in_db
from utils.scan_for_vulns import scan_for_vulns
from utils.data_adapter import data_adapter
from utils.save_results_as_json import save_results_as_json
from utils.obtain_cve_info_from_api import obtain_cve_info_from_api
from utils.get_default_gateway import get_default_gateway
from utils.db_connection import db_connection
from utils.get_db_results import get_db_results
from utils.get_db_results_filter import get_db_results_filter
from utils.obtain_isp_info_from_api import obtain_isp_info_from_api
from utils.obtain_user_collection import obtain_user_collection
from utils.get_db_reports import get_db_reports

# * ========= API ========= *#

from api.reports.get_top_cve import get_top_cve
from api.reports.get_top_isp import get_top_isp
from api.reports.get_top_vendor import get_top_vendor
from api.reports.get_top_vendor_cve import get_top_vendor_cve
from api.reports.get_top_ip import get_top_ip
from api.reports.get_top_isp_cve import get_top_isp_cve
from api.reports.get_top_port_cve import get_top_port_cve
from api.reports.get_top_ip_scanning_time import get_top_ip_scanning_time


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/scan", methods=["POST"])
def scan():
    userId = request.get_json()["userId"]
    gateway = get_default_gateway()
    start_time = time.time()

    scan_results = scan_for_vulns(gateway, "nmap -sV --script vulners")
    save_results_as_json(scan_results, "1-scan_results.json")

    scan_results_adapted = data_adapter(scan_results, gateway, userId)
    scan_results_adapted = obtain_isp_info_from_api(scan_results_adapted)
    collection = db_connection()

    if len(scan_results_adapted["vulnerabilities"]) == 0:
        # save_results_in_db(collection, scan_results_adapted)
        end_time = time.time()
        elapsed_time = end_time - start_time
        scan_results_adapted["scanningTime"] = elapsed_time
        save_results_as_json(scan_results_adapted, "2-scan_results_adapted.json")
        save_results_in_db(collection, scan_results_adapted)

        return jsonify(scan_results_adapted)

    scan_results_adapted_cve_info = obtain_cve_info_from_api(scan_results_adapted)

    end_time = time.time()
    elapsed_time = end_time - start_time
    scan_results_adapted_cve_info["scanningTime"] = elapsed_time

    save_results_as_json(
        scan_results_adapted_cve_info, "3-scan_results_adapted_cve_info.json"
    )
    save_results_in_db(collection, scan_results_adapted_cve_info)

    return jsonify(scan_results_adapted_cve_info)


@app.route("/scan/all")
def getAllScans():
    collection = db_connection()
    results = get_db_results(collection)

    return results


@app.route("/scan/filter", methods=["POST"])
def getScanByFilter():
    collection = db_connection()
    results = get_db_results_filter(collection)

    return results


@app.route("/register", methods=["POST"])
def register_user():
    try:
        users_collection = obtain_user_collection()

        user_data = request.get_json()

        existent_user = users_collection.find_one({"email": user_data["email"]})

        if existent_user:
            return jsonify({"error": "El Usuario ya existe"}), 400

        hashed_password = bcrypt.hashpw(
            user_data["password"].encode("utf-8"), bcrypt.gensalt()
        )

        users_collection.insert_one(
            {
                "name": user_data["name"],
                "email": user_data["email"],
                "role": user_data["role"] if "role" in user_data else "USER",
                "asn": user_data["asn"] if "asn" in user_data else None,
                "password": hashed_password,
            }
        )

        return jsonify({"message": "Usuario creado exitosamente"}), 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error al crear el usuario"}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        # Obtiene los datos de inicio de sesión del cuerpo de la solicitud
        login_data = request.get_json()

        users_collection = obtain_user_collection()

        # Busca el usuario en la base de datos por su correo electrónico
        user = users_collection.find_one({"email": login_data["email"]})

        if user:
            # Compara la contraseña proporcionada con la contraseña almacenada en la base de datos
            if bcrypt.checkpw(login_data["password"].encode("utf-8"), user["password"]):
                return (
                    jsonify(
                        {
                            "message": "Inicio de sesión exitoso",
                            "user": {
                                "_id": str(user["_id"]),
                                "name": user["name"],
                                "email": user["email"],
                                "role": user["role"],
                                "asn": user["asn"],
                            },
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Credenciales incorrectas"}), 401
        else:
            return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Error al iniciar sesión"}), 500


# Reports


@app.route("/reports")
def reports():
    collection = db_connection()
    results = get_db_reports(collection)
    return results


@app.route("/reports/cve")
def api_get_top_cve():
    return get_top_cve()


@app.route("/reports/ip")
def api_get_top_ip():
    return get_top_ip()

@app.route("/reports/ip/scanning_time")
def api_get_top_ip_scanning_time():
    return get_top_ip_scanning_time()

@app.route("/reports/isp")
def api_get_top_isp():
    return get_top_isp()


@app.route("/reports/isp/cve")
def api_get_top_isp_cve():
    return get_top_isp_cve()

@app.route("/reports/port/cve")
def api_get_top_port_cve():
    return get_top_port_cve()


@app.route("/reports/vendor")
def api_get_top_vendor():
    return get_top_vendor()


@app.route("/reports/vendor/cve")
def api_get_top_vendor_cve():
    return get_top_vendor_cve()


if __name__ == "__main__":
    app.run(debug=True, port=3000)
