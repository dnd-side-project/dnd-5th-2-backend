from flask import Blueprint, jsonify, request


def create_supplements_blueprint(services):
    supplements_service = services.supplements_service

    supplements_bp = Blueprint("supplements", __name__, url_prefix="/supplements")

    @supplements_bp.route("/<int:supplement_id>", methods=["GET"])
    def info(supplement_id):
        info = supplements_service.get_supplement_info(supplement_id)
        if info is None:
            return "존재하지 않는 영양제입니다", 404
        return jsonify(info)

    @supplements_bp.route("/search")
    def search():
        supplement_name = request.args.get("supplementName")
        type = request.args.get("type")
        tag = request.args.get("tag")
        results = supplements_service.search_supplements(supplement_name, type, tag)
        return jsonify(results)

    return supplements_bp
