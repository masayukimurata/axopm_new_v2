import psycopg2.extras
from decimal import Decimal
from typing import List, Dict, Any, Tuple, cast
from psycopg2.extensions import connection as PgConnection

class MurataRecipeEngine:
    def __init__(self):
        """db_urlを引数から削除。接続はメソッド呼び出し時に注入される"""
        pass

    def calculate_cost_recursive(
        self,
        conn: PgConnection,
        r_id: int
    ) -> Tuple[Decimal, List[Dict[str, Any]]]:
        """
        外部から取得したデータベース接続(conn)を利用して原価計算を行う。
        接続のオープン・クローズは呼び出し元(main.py等)が管理する。
        """
        # 外部から受け取ったコネクションでカーソルを生成
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            query = """
                SELECT i.m_id, i.usage_amount, m.unit_cost, m.is_internal_product, m.m_name,
                       r.serving_size
                FROM public.t_recipe_ingredients i
                JOIN public.t_merchandise_pro m ON i.m_id = m.m_id
                LEFT JOIN public.t_recipes r ON (
                    m.is_internal_product = true AND
                    r.r_id = CAST(NULLIF(REGEXP_REPLACE(m.m_id, '[^0-9]', '', 'g'), '') AS INTEGER)
                )
                WHERE i.r_id = %s AND m.is_active = true
                ORDER BY i.m_id
            """
            cur.execute(query, (r_id,))
            ingredients = cast(List[Dict[str, Any]], cur.fetchall())

            if not ingredients:
                return Decimal('0.00'), []

            total_cost = Decimal('0.00')
            details: List[Dict[str, Any]] = []

            for item in ingredients:
                qty = Decimal(str(item.get('usage_amount') or '0'))
                is_internal = bool(item.get('is_internal_product'))

                if is_internal:
                    m_id_str = str(item.get('m_id', ''))
                    numeric_id_str = ''.join(filter(str.isdigit, m_id_str))
                    sub_r_id = int(numeric_id_str)

                    # 注入された接続(conn)を再帰的に受け渡す
                    sub_total_cost, _ = self.calculate_cost_recursive(conn, sub_r_id)

                    weight_val = item.get('serving_size')
                    total_weight = weight_val if weight_val is not None else Decimal('1.0')
                    unit_price = sub_total_cost / total_weight if total_weight > 0 else Decimal('0.00')
                else:
                    unit_price = Decimal(str(item.get('unit_cost') or '0.00'))

                line_cost = qty * unit_price
                total_cost += line_cost

                details.append({
                    "m_name": str(item.get('m_name')),
                    "quantity": float(qty),
                    "unit_price": float(unit_price),
                    "line_cost": float(line_cost)
                })

            return total_cost, details
