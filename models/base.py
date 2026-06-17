from typing import Type, Dict, Any, List

# モデルを登録するためのグローバルレジストリ
MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_model(
    label: str,
    icon: str,
    table_name: str,
    order: int = 99,
    menu_group: str = "基本",
    doc_rule: str = "",
    schema: str = "public"
):
    """
    モデルに運用情報（順序・グループ・注意書き・テーブル定義）を付与するデコレータ
    """
    def decorator(cls: Type):
        MODEL_REGISTRY[cls.__name__] = {
            "model": cls,
            "label": label,
            "icon": icon,
            "table_name": table_name,
            "order": order,
            "menu_group": menu_group,
            "doc_rule": doc_rule,
            "schema": schema
        }
        # クラス属性へのセット
        setattr(cls, "_label", label)
        setattr(cls, "_icon", icon)
        setattr(cls, "_table_name", table_name)
        setattr(cls, "_order", order)
        setattr(cls, "_menu_group", menu_group)
        setattr(cls, "_doc_rule", doc_rule)
        setattr(cls, "_schema", schema)
        return cls
    return decorator

def get_registered_models() -> List[Type]:
    """登録されたモデルをorder順にソートして返す"""
    sorted_registry = sorted(MODEL_REGISTRY.values(), key=lambda x: x["order"])
    return [item["model"] for item in sorted_registry]

class BaseModel:
    """
    すべてのデータモデルの基底クラス
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
