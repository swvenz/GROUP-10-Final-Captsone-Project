import pandas as gt

gt.DataFrame(columns=[
    'product_id', 'product_name', 'category', 'price', 'stock_quantity', 'reorder_level'
]).to_excel("products.xlsx", index=False)

gt.DataFrame(columns=[
    'movement_id', 'product_id', 'movement_type', 'quantity', 'date', 'remarks'
]).to_excel("inventory_movements.xlsx", index=False)

gt.DataFrame(columns=[
    'sale_id', 'date', 'product_id', 'quantity_sold', 'unit_price', 'total_amount'
]).to_excel("sales.xlsx", index=False)

print("CREATED")