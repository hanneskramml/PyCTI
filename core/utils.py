from flask_sqlalchemy import inspect


def get_dict_from_object(obj):
    return {column.key: getattr(obj, column.key)
            for column in inspect(obj).mapper.column_attrs}
