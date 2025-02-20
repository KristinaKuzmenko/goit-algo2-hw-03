import pandas as pd
import timeit
from BTrees.OOBTree import OOBTree

def load_data(file_path):
    try:
        return pd.read_csv(file_path).to_dict(orient='records')
    except Exception:
        print("File not found")

# Add an item to the BTree using its price as the key.
# Price is chosen as the key because it enables efficient range queries
# allowing quick lookup of items within a specific price interval using items(min_price, max_price) method
def add_item_to_tree(tree, item):
    price = float(item['Price'])
    if price not in tree:
        tree[price] = []
    tree[price].append(item)

# Add an item to a regular dictionary using its ID as the key
def add_item_to_dict(dict, item):
    dict[item['ID']] = {
        'Name': item['Name'],
        'Category': item['Category'],
        'Price': item['Price']
    }

# Perform a range query on the BTree using items(min, max) method
def range_query_tree(tree, min_price, max_price):
    return [item for _, item in tree.items(min_price, max_price)]

# Perform a range query on the dictionary by filtering each item (linear search)
def range_query_dict(dict, min_price, max_price):
    return [item for item in dict.values() if min_price <= item['Price'] <= max_price]

def main():
    # Initialize the BTree and dictionary
    tree = OOBTree()
    dict = {}

    file_path = 'generated_items_data.csv'
    data = load_data(file_path)

    if data:
        # Insert each item into both the tree and the dictionary
        for item in data:
            add_item_to_tree(tree, item)
            add_item_to_dict(dict, item)

        # Define the price range for the query
        min_price = 50
        max_price = 100

        num_queries = 100

        # Measure the time it takes to execute the range queries on both data structures
        tree_time = timeit.timeit(lambda: range_query_tree(tree, min_price, max_price), number=num_queries)
        dict_time = timeit.timeit(lambda: range_query_dict(dict, min_price, max_price), number=num_queries)

        print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
        print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == '__main__':
    main()