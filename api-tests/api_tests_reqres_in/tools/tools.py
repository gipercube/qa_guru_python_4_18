def data_len(response):
    dat_len = 0
    for i in response["data"]:
        if i == "id":
            dat_len += 1
    return dat_len


def get_date(value):
    return value[:10]
