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
        get_args = request.args.get
        supplement_name = get_args("supplementName")
        type = get_args("type")
        tag = get_args("tag")
        page = int(get_args("page"))
        if page is None:
            page = 1
        results = supplements_service.search_supplements(
            supplement_name, type, tag, page
        )
        return jsonify(results)

    return supplements_bp
