import csv

def extract_and_write_data():
    """ Extract the datas needed for the tables Product and Category
    and write them in two csv"""

    categories = []
    products = []

    with open('openfoodfacts.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            if row['product_name'] and \
            row['categories'] and \
            row['image_url'] and \
            row['nutrition_grade_fr']:

                    current_categories = row['categories'].split(', ')[:3]
                    if current_categories not in categories and \
                    len(current_categories) == 3:
                        categories.append(current_categories)

                        products.append([
                            row['product_name'],
                            row['nutrition_grade_fr'],
                            row['image_url'],
                            row['purchase_places'],
                            row['energy_100g'],
                            row['fat_100g'],
                            row['saturated-fat_100g'],
                            row['carbohydrates_100g'],
                            row['sugars_100g'],
                            row['fiber_100g'],
                            row['proteins_100g'],
                            ]
                            )
        with open('categories.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(categories)
        with open('products.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(products)

if __name__ == '__main__':
    extract_and_write_data()