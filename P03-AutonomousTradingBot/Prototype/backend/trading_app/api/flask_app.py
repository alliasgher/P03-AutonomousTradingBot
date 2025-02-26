import datetime
from flask import Flask, request, jsonify
from ..entrypoint import commands, unit_of_work
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


app = Flask(__name__)
app.config["JWT_SECRET_KEY"]= "super-secret"
jwt = JWTManager(app)
prefix = "/api/v1"

@app.route(prefix)
def hello():
    return "Welcome to the autonomous trading bot!", 200


@app.route(prefix+"/create-analyst", methods=["POST"])
def create_analyst():
    try:
        commands.create_analyst(
            request.json["name"],
            request.json["address"],
            request.json["email"],
            request.json["phone_number"],
            request.json["password"],
            unit_of_work.UnitOfWork(),
        )
        responseData = {"success": True, "message": "Analyst created successfully!"}
        return jsonify(responseData), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400
    


@app.route(prefix+"/analyst-login", methods=["POST"])
def analyst_login():
    email = request.json["email"]
    password = request.json["password"]
    try:
        ret = commands.analyst_login(
            email,
            password,
            uow=unit_of_work.UnitOfWork(),
        )
        # expires in 1hr
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=1))
        retObj = ret.__dict__
        retObj["access_token"] = access_token
        retObj["token_type"] = "bearer"
        retObj["expires_in"] = 3600
        
        return jsonify(retObj), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 401


@app.route(prefix+"/analyst-logout", methods=["POST"])
@jwt_required()
def analyst_logout():
    email = get_jwt_identity()
    commands.analyst_logout(
        email,
        uow=unit_of_work.UnitOfWork(),
    )
    retObj = {"success": True, "message": "Analyst logged out successfully!"}
    return jsonify(retObj), 200


@app.route(prefix+"/register-investor", methods=["POST"])
@jwt_required()
def register_investor():
    try:
        ret = commands.register_investor(
            request.json["name"],
            request.json["address"],
            request.json["investor_email"],
            request.json["phone_number"],
            request.json["analyst_email"],
            unit_of_work.UnitOfWork(),
        )
        return jsonify(ret), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route(prefix + "/investor-login", methods=["POST"])
def investor_login():
    email = request.json["email"]
    try:
        ret = commands.investor_login(
            email,
            request.json["password"],
            uow=unit_of_work.UnitOfWork(),
        )
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=1))
        retObj = ret.__dict__
        retObj["access_token"] = access_token
        retObj["token_type"] = "bearer"
        retObj["expires_in"] = 3600
        return jsonify(retObj), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 401


@app.route(prefix + "/investor-logout", methods=["POST"])
@jwt_required()
def investor_logout():
    email = get_jwt_identity()
    commands.investor_logout(
        email,
        uow=unit_of_work.UnitOfWork(),
    )
    retObj = {"success": True, "message": "Investor logged out successfully!"}
    return jsonify(retObj), 200


# """
# Bot module
# """


@app.route(prefix + "/add-bot", methods=["POST"])
@jwt_required()
def add_bot():
    analyst_email = get_jwt_identity()
    # get analyst id   
    analyst = commands.get_analyst(analyst_email, uow=unit_of_work.UnitOfWork()) 
    analyst_id = analyst.id

    commands.add_bot(
        analyst_id,
        request.json["investor_id"],
        request.json["trades"],
        request.json["assigned_model"],
        request.json["risk_appetite"],
        request.json["target_return"],
        request.json["duration"],
        uow=unit_of_work.UnitOfWork(),
    )

    retObj = {"success": True, "message": "Bot added successfully!"}
    return jsonify(retObj), 200




# @app.route(prefix + "/initiate-bot-execution", methods=["POST"])
# def initiate_bot_execution():
#     commands.initiate_bot_execution(
#         request.json["bot_id"],
#         uow=unit_of_work.UnitOfWork(),
#     )
#     return "OK", 200


# @app.route(prefix + "/terminate-bot", methods=["POST"])
# def terminate_bot():
#     commands.terminate_bot(
#         request.json["bot_id"],
#         uow=unit_of_work.UnitOfWork(),
#     )
#     return "OK", 200
