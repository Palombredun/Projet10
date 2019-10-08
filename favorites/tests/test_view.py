from django.test import TestCase, Client
from django.contrib.auth.models import User

from products.models import Category, Product

class FavoritePageTest(TestCase):
	def setUp(self):
		c = Category.objects.create(
			category_name='test_category'
			)
		c.save()
		Product.objects.create(
			product_name='test1',
			nutriscore='e',
			image_url='https://test_image.com',
			product_url='https://testopenfoodfacts.org',
			category = c
			)
		self.product = Product.objects.get(product_name='test1')

		User.objects.create_user(
			username='test_user',
			email='test_email@mail.com',
			password='test_userpassword123'
			)
		self.user = User.objects.first()
		self.product.favorite.add(self.user)
		self.login_infos = {'username':'test_user', 'password':'test_userpassword123'}

	def test_uses_favorite_template_logged_in(self):
		c = Client()
		response = c.post('/utilisateur/connexion/', self.login_infos)
		response = c.get('/utilisateur/favoris/')
		self.assertTemplateUsed(response, 'favorites/favorites.html')

	def test_favorite_correctly_saved(self):
		c = Client()
		response = c.post('/utilisateur/connexion/', self.login_infos)
		response = c.get('/utilisateur/favoris/')
		content = response.content.decode('utf8')
		self.assertInHTML("""<p class="product-name" id="test1">test1</p>""", content)

	def test_cannot_save_twice_same_product(self):
		self.product.favorite.add(self.user)
		c = Client()
		response = c.post('/utilisateur/connexion/', self.login_infos)
		response = c.get('/utilisateur/favoris/')
		content = response.content.decode('utf8')
		self.assertInHTML("""<p class="product-name" id="test1">test1</p>""", content)
