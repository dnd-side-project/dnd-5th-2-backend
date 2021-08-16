class SupplementsService:
    def __init__(self, supplements_dao):
        self.supplements_dao = supplements_dao

    def get(self, supplement_id):
        data = self.supplements_dao.get(supplement_id)
        if data is None:
            return None
        data = data._asdict()
        data["supplement_id"] = data["id"]
        data.pop("id")
        return data

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

        results = [result._asdict() for result in results]
        for result in results:
            result["supplement_id"] = result["id"]
            result.pop("id")
        return results

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
