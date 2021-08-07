from .utils import to_camel_dict


class SupplementsService:
    def __init__(self, supplements_dao):
        self.supplements_dao = supplements_dao

    def get(self, supplement_id):
        data = self.supplements_dao.get(supplement_id)
        if data is None:
            return None
        camel_data = to_camel_dict(data)
        camel_data["supplementId"] = data["id"]
        return camel_data

    def search(self, supplement_name, type, tag, page):
        # 제품명 검색
        if supplement_name is not None:
            results = self.supplements_dao.search_by_name(supplement_name, page)

        # 유형별 검색
        if type is not None:
            tags = [tag["tag_name"] for tag in self.supplements_dao.get_type_tags(type)]
            results = self.supplements_dao.search_by_tags(tags, page)

        # 기능별 검색
        if tag is not None:
            results = self.supplements_dao.search_by_tag(tag, page)

        new_results = []
        for result in results:
            new_result = to_camel_dict(result)
            new_result["supplementId"] = result["id"]
            new_results.append(new_result)
        return new_results

    def exists_type(self, type):
        data = self.supplements_dao.get_type(type)
        if data is None:
            return False
        return True

    def exists_tag(self, tag):
        data = self.supplements_dao.get_tag(tag)
        if data is None:
            return False
        return True
