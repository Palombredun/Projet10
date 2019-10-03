import os
import json

from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = "Update the database with the csv contained in the directory products/data"

    def extract_data(self):
        data = []
        json_data = []

        for json_file in os.listdir('update/data'):
            if "json" in json_file:
                file = "update/data/" + json_file
                with open(file, "r") as f:
                    data = f.read()
                    ldata = data.split("\n")
                    for elt in ldata:
                        if elt: 
                            json_data.append(json.loads(elt))
        return json_data


    def category_set(self):
        categories_created = Category.objects.all()
        result = set([])
        for category in categories_created:
            result.add((category.top_category, 
                        category.middle_category,
                        category.bottom_category)
            )
        return result
    def handle(self, *args, **kwargs):
        categories_created = self.category_set()
        
        json_data = self.extract_data()

        for row in json_data:
            if (row.get('product_name') and
                row.get('categories') and
                row.get('image_url') and
                row.get('nutrition_grade_fr')) in row.keys():
                print(row.keys())
                # if the line has the minimum of informations required:
                current_category = tuple(row['categories'].split(', ')[:3])
                if len(current_category) == 3:
                    if current_category not in categories_created:
                        categories_created.add(current_category)
                        new_category = Category.objects.create(
                            top_category=current_category[0],
                            middle_category=current_category[1],
                            bottom_category=current_category[2]
                            )
                    
                    category = Category.objects.filter(
                        top_category=current_category[0]
                    ).filter(
                        middle_category=current_category[1]
                    ).filter(
                        bottom_category=current_category[2]
                    )[0]
                    print(row['product_name'])
                    try:
                        purchase_places = row['purchase_places']
                    except:
                        purchase_places = ''
                    try:
                        energy_100g = float(row['energy_100g'])
                    except:
                        energy_100g = -1.
                    try:
                        fat_100g = float(row['fat_100g'])
                    except:
                        fat_100g = -1.
                    try:
                        saturated_fats_100g = float(row['saturated-fat_100g'])
                    except:
                        saturated_fats_100g = -1.
                    try:
                        carbohydrates_100g = float(row['carbohydrates_100g'])
                    except:
                        carbohydrates_100g = -1.
                    try:
                        sugars_100g = float(row['sugars_100g'])
                    except:
                        sugars_100g = -1.
                    try:
                        fiber_100g = float(row['fiber_100g'])
                    except:
                        fiber_100g = -1.
                    try:
                        proteins_100g = float(row['proteins_100g'])
                    except:
                        proteins_100g = -1.
                    try:
                        salt_100g = float(row['salt_100g'])
                    except:
                        salt_100g = -1.
                    
                    new_product = Product.objects.create(
                        product_name=row['product_name'],
                        nutriscore=row['nutrition_grade_fr'],
                        image_url=row['image_url'],
                        product_url = row['url'],
                        category=category,
                        purchase_places=purchase_places,
                        energy_100g=energy_100g,
                        fat_100g=fat_100g,
                        saturated_fats_100g=saturated_fats_100g,
                        carbohydrates_100g=carbohydrates_100g,
                        sugars_100g=sugars_100g,
                        fibers_100g=fiber_100g,
                        proteins_100g=proteins_100g,
                        salt_100g=salt_100g)    