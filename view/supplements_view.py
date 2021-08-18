from flask import Blueprint, jsonify, request


def create_supplements_blueprint(services):
    supplements_service = services.supplements_service

    supplements_bp = Blueprint("supplements", __name__, url_prefix="/supplements")

    @supplements_bp.route("/<int:supplement_id>", methods=["GET"])
    def info(supplement_id):
        info = supplements_service.get(supplement_id)
        if info is None:
            return jsonify({"message": "존재하지 않는 영양제입니다"}), 404
        return jsonify(info)

    @supplements_bp.route("/search", methods=["GET"])
    def search():
        get_arg = request.args.get
        supplement_name = get_arg("supplementName")
        type = get_arg("type_tag")
        tag = get_arg("tag")
        page_size = get_arg("limit")
        page = get_arg("page")

        if type is not None and supplements_service.exists_type(type) is False:
            return jsonify({"message": "존재하지 않는 타입입니다"}), 404
        if tag is not None and supplements_service.exists_tag(tag) is False:
            return jsonify({"message": "존재하지 않는 기능입니다"}), 404
        if page_size is None:
            page_size = "10"
        if page_size.isnumeric() is False:
            return jsonify({"message": "잘못된 페이지 크기 입니다"}), 400
        if page is None:
            page = "1"
        if page.isnumeric() is False:
            return jsonify({"message": "잘못된 페이지 숫자 입니다"}), 400

        # page를 제외한 arg는 한번에 하나만 요청 가능
        arg_count = 0
        for arg in (supplement_name, type, tag):
            if arg is not None:
                arg_count += 1
        if arg_count > 1 or arg_count == 0:
            return jsonify({"message": "잘못된 요청입니다"}), 400

        page_size = int(page_size)
        page = int(page)
        results = supplements_service.search(
            supplement_name, type, tag, page_size, page
        )
        return jsonify(results)

    return supplements_bp
