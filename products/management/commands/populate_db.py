import csv

from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = "Populate the database with the products previously downloaded."

    def handle(self, *args, **options):
        products_created = []
        categories_created = set([])
        
        with open('products/management/commands/openfoodfacts.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                if row['product_name'] and \
                row['categories'] and \
                row['image_url'] and \
                row['nutrition_grade_fr']:
    
                    current_category = tuple(row['categories'].split(', ')[:3])
                    if len(current_category) == 3 and\
                        row['product_name'] not in products_created:

                        categories_created.add(current_category)
                        new_category = Category.objects.create(
                            top_category=current_category[0],
                            middle_category=current_category[1],
                            bottom_category=current_category[2]
                            )

                        category_reference = Category.objects.get(
                            top_category=current_category[0],
                            middle_category=current_category[1],
                            bottom_category=current_category[2]
                            )
                        products_created.append(row['product_name'])
                        try:
                            purchase_places = row['purchase_places']
                        except:
                            purchase_places = ''
                        try:
                            energy_100g = row['energy_100g']
                        except:
                            energy_100g = -1
                        try:
                            fat_100g = row['fat_100g']
                        except:
                            fat_100g = -1
                        try:
                            saturated_fats_100g = row['saturated-fat_100g']
                        except:
                            saturated_fats_100g = -1
                        try:
                            carbohydrates_100g = row['carbohydrates_100g']
                        except:
                            carbohydrates_100g = -1
                        try:
                            sugars_100g = row['sugars_100g']
                        except:
                            sugars_100g = -1
                        try:
                            fiber_100g = row['fiber_100g']
                        except:
                            fiber_100g = -1
                        try:
                            salt_100g = float(row['salt_100g'])
                        except:
                            salt_100g = -1
                        try:
                            proteins_100g = row['proteins_100g']
                        except:
                            proteins_100g = -1

                        new_product = Product.objects.create(
                            product_name=row['product_name'],
                            nutriscore=row['nutrition_grade_fr'],
                            image_url=row['image_url'],
                            product_url = row['url'],
                            category=category_reference,
                            purchase_places=purchase_places,
                            energy_100g=energy_100g,
                            fat_100g=fat_100g,
                            saturated_fats_100g=saturated_fats_100g,
                            carbohydrates_100g=carbohydrates_100g,
                            sugars_100g=sugars_100g,
                            fibers_100g=fiber_100g,
                            proteins_100g=proteins_100g,
                            salt_100g=salt_100g,
                            )