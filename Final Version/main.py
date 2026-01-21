import pandas as pd
from datetime import datetime

PRODUCTS_FILE = "products.xlsx"
SALES_FILE = "sales.xlsx"
MOVEMENTS_FILE = "inventory_movements.xlsx"

# Basic menu options
def menu():
    print("\n--- SALES & INVENTORY SYSTEM ---")
    print("1. View Products")
    print("2. Add Product")
    print("3. Record Sale")
    print("4. Restock Sale")
    print("5. Exit program")

# View products in the excel (.xlsx) file
def view_products():
    df = pd.read_excel(PRODUCTS_FILE)

    print("\n--- PRODUCT LIST ---")

    if df.empty:
        print("No products yet.")
        return

    print(df)

    print("\n--- STOCK STATUS ---")
    
    #Gives out an alert for stock products that are going low (below 10)
    low_stock = df[df['stock_quantity'] < 10]
    
    if not low_stock.empty:
        print("\n-- LOW STOCK --:")
        for _, row in low_stock.iterrows():
            print(f"  • {row['product_name']} (ID: {row['product_id']}): {row['stock_quantity']} units")
    
    #Shows a product/s if it has sufficient stock items (10 or above)
    sufficient_stock = df[df['stock_quantity'] >= 10]
    
    if not sufficient_stock.empty:
        print("\n-- SUFFICIENT STOCK --:")
        for _, row in sufficient_stock.iterrows():
            print(f"  • {row['product_name']} (ID: {row['product_id']}): {row['stock_quantity']} units")
    
#Gives out an alert to see if their are stocks that are low
    print("\n--- INSUFFICIENT STOCK ALERTS ---")
    low_stock = df[df['stock_quantity'] <= 0]

    if low_stock.empty:
        print("All products have sufficient stock.")
    else:
        for _, row in low_stock.iterrows():
            print(
                f"Product ID: {row['product_id']} "
                f"({row['product_name']}) has INSUFFICIENT stock "
                f"[Stock: {row['stock_quantity']}, Reorder Level: {row['reorder_level']}]"
                )

# Add one product to the excel (.xlsx) file
def add_product():
    df = pd.read_excel(PRODUCTS_FILE)

    new_product = {
        "product_id": input("Product ID: "),
        "product_name": input("Name: "),
        "category": input("Category: "),
        "price": float(input("Price: ")),
        "stock_quantity": check_stock_level(input("Stock: ")),
        "reorder_level": int(input("Reorder Level: "))
    }

    df = pd.concat([df, pd.DataFrame([new_product])], ignore_index=True)
    df.to_excel(PRODUCTS_FILE, index=False)
    print("Product added successfully.")

# This allows the add_product funtion to detect if the inputted stock level is either zero or a negative value
def check_stock_level(stock):
    try:
        stock_int = int(stock)
        if stock_int < 0:
            print("Error: Stock cannot be negative. Setting to 0.")
            return 0
        return stock_int
    except ValueError:
        print("Error: Invalid input. Setting stock to 0.")
        return 0
# If it is not an integer, also immediately set the stock to 0

#Record sales of the product
def record_sale():
    products = pd.read_excel(PRODUCTS_FILE)
    sales = pd.read_excel(SALES_FILE)
    movements = pd.read_excel(MOVEMENTS_FILE)

    pid = input("Product ID: ")
    qty = int(input("Quantity to sell: "))

    if pid not in products['product_id'].astype(str).values:
        print("Product not found.")
        return

    idx = products[products['product_id'].astype(str) == pid].index[0]

    if products.loc[idx, 'stock_quantity'] < qty:
        print("Not enough stock.")
        return

    products.loc[idx, 'stock_quantity'] -= qty
    products.to_excel(PRODUCTS_FILE, index=False)

    unit_price = products.loc[idx, 'price']
    total = unit_price * qty

#Records the product transaction in the sales.xlsx
    new_sale = {
        'sale_id': len(sales) + 1,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'product_id': pid,
        'quantity_sold': qty,
        'unit_price': unit_price,
        'total_amount': total
    }

    sales = pd.concat([sales, pd.DataFrame([new_sale])], ignore_index=True)
    sales.to_excel(SALES_FILE, index=False)

#Records the date of the transaction in the inventory_movement.xlsx
    new_move = {
        'movement_id': len(movements) + 1,
        'product_id': pid,
        'movement_type': 'OUT',
        'quantity': qty,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'remarks': 'Sale'
    }

    movements = pd.concat([movements, pd.DataFrame([new_move])], ignore_index=True)
    movements.to_excel(MOVEMENTS_FILE, index=False)

    print("Sale recorded successfully!")

#Restocks the quantity of a product
def restock_product():
    products = pd.read_excel(PRODUCTS_FILE)
    movements = pd.read_excel(MOVEMENTS_FILE)

    pid = input("Product ID to restock: ")
    qty = int(input("Quantity to add: "))

    if pid not in products['product_id'].astype(str).values:
        print("Product not found.")
        return

    idx = products[products['product_id'].astype(str) == pid].index[0]
    
    products.loc[idx, 'stock_quantity'] += qty
    products.to_excel(PRODUCTS_FILE, index=False)

#Records the date of the restock in the inventory_movement.xlsx
    new_move = {
        'movement_id': len(movements) + 1,
        'product_id': pid,
        'movement_type': 'IN',
        'quantity': qty,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'remarks': 'Restock'
    }

    movements = pd.concat([movements, pd.DataFrame([new_move])], ignore_index=True)
    movements.to_excel(MOVEMENTS_FILE, index=False)

    print("Stock updated successfully!")

# --- MAIN PROGRAM ---
while True:
    menu()
    choice = input("Choose: ")

    if choice == "1":
        view_products()
    elif choice == "2":
        add_product()
    elif choice == "3":
        record_sale()
    elif choice == "4":
        restock_product()
    elif choice == "5":
        print("Exiting program.")
        break
    else:
        print("Invalid option. Try again.")