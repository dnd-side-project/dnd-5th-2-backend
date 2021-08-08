def to_camel(snake_string):
    components = snake_string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


# snake_case로 키가 구성된 dictionary를 camelCase로 변환
def to_camel_dict(snake_dict):
    camel_dict = {}
    for snake_key, value in snake_dict.items():
        if snake_key == "id":
            continue

        camel_key = to_camel(snake_key)
        camel_dict[camel_key] = value
    return camel_dict
