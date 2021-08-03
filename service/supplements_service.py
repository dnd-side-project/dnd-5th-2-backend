class SupplementsService:
    def __init__(self, supplements_dao):
        self.supplements_dao = supplements_dao

    def get_supplement_info(self, supplement_id):
        # 페이지네이션 필요
        info = self.supplements_dao.get_supplement_info(supplement_id)
        if info is None:
            return info

        info_dict = {}
        info_dict["supplementId"] = info[0]
        info_dict["supplementName"] = info[1]
        info_dict["companyName"] = info[2]
        info_dict["ratings"] = info[3]
        return info_dict

    def search_supplements(self, supplement_name, type, tag, page):
        # 페이지네이션 필요
        if supplement_name is not None:
            results = self.supplements_dao.search_supplements_by_name(
                supplement_name, page
            )
        elif type is not None:
            tags = {}
            tags = [tag[0] for tag in self.supplements_dao.get_type_tags(type)]
            results = self.supplements_dao.search_supplements_by_tags(tags, page)
        elif tag is not None:
            results = self.supplements_dao.search_supplements_by_tag(tag, page)

        new_results = []
        for result in results:
            new_result = {}
            new_result["supplementId"] = result[0]
            new_result["supplementName"] = result[1]
            new_result["companyName"] = result[2]
            new_result["ratings"] = result[3]
            new_results.append(new_result)
        return new_results
