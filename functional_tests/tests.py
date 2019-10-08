from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

import time

from products.models import Category, Product


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

        category = Category(category_name='petits déjeuners')
        category.save()
        nutella = Product(
            product_name='nutella',
            nutriscore='e',
            image_url='https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.400.jpg',
            product_url='https://fr.openfoodfacts.org/produit/3017620422003/nutella-ferrero',
            category=category
            )
        nutella.save()
        nutella_ersatz_1 = Product(
            product_name='ersatz_nutella_1',
            nutriscore='c',
            category=category
            )
        nutella_ersatz_1.save()
        nutella_ersatz_2 = Product(
            product_name='ersatz_nutella_2',
            nutriscore='b',
            category=category
            )
        nutella_ersatz_2.save()
        nutella_ersatz_3 = Product(
            product_name='ersatz_nutella_3',
            nutriscore='b',
            category=category
            )
        nutella_ersatz_3.save()
        nutella_ersatz_4 = Product(
            product_name='ersatz_nutella_4',
            nutriscore='a',
            category=category
            )
        nutella_ersatz_4.save()
        nutella_ersatz_5 = Product(
            product_name='ersatz_nutella_5',
            nutriscore='d',
            category=category
            )
        nutella_ersatz_5.save()
        nutella_ersatz_6 = Product(
            product_name='ersatz_nutella_6',
            nutriscore='c',
            category=category
            )
        nutella_ersatz_6.save()

    def tearDown(self):
        self.browser.quit()

    def visit_signup_page(self):
        login = self.browser.find_element_by_class_name('login')
        login.click()
        signup = self.browser.find_element_by_class_name('signup-link')
        signup.click()

    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online food app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention the title of the app
        # and its motto
        self.assertIn('Pur Beurre', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('DU GRAS OUI, MAIS DE QUALITÉ !', header_text)

        # She tries the research form in the homepage :
        inputbox = self.browser.find_element_by_id('input-home')
        inputbox.send_keys('nutella')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(5)

        # Edith is sent to the page containing alternative products
        # to the one she searched (indicated in the top of the page)
        self.assertIn('Recherche', self.browser.title)
        # A message prevents her that she as to be connected if she wants
        # to save her favorite products
        message = self.browser.find_element_by_class_name('replacement').text
        self.assertIn('Vous devez avoir un compte pour sauvegarder des aliments', 
            message)

        # Disappointed by this, she leaves for now but promises
        # herself she will come back

    def test_create_account_and_visit_profile(self):
        # Edith has come back but has little time on her hand,
        # today she will only try to create an account and visit
        # the pages related to the user
        self.browser.get(self.live_server_url)

        # she clicks on the login icon in the navbar
        login = self.browser.find_element_by_class_name('login')
        login.click()
        self.assertIn('Connexion', self.browser.title)

        # Since Edith does not have an account yet, she has to create it
        # and so, click on the link at the bottom of the login form
        signup = self.browser.find_element_by_class_name('signup-link')
        signup.click()
        self.assertIn('Inscription', self.browser.title)

        # Now that she has reached the front page, she creates her account :
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('Edith')
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys('edith@mail.com')
        password1_input = self.browser.find_element_by_name('password1')
        password1_input.send_keys('Edithpassword')
        password2_input = self.browser.find_element_by_name('password2')
        password2_input.send_keys('Edithpassword')
        button = self.browser.find_element_by_tag_name('button')
        button.click()

        # She is redirected to the home page
        # she notices the navbar has changed, three icons have appeared
        self.assertIn('Pur Beurre', self.browser.title)
        try:
            icons = self.browser.find_element_by_tag_name('svg')
        except:
            print('NoSuchElementException')

        #She clicks on the profile page :
        profile_page = self.browser.find_element_by_class_name('profile')
        profile_page.click()
        self.assertIn('Profil', self.browser.title)
        username = self.browser.find_element_by_class_name('username').text
        self.assertEqual('Edith', username)
        email = self.browser.find_element_by_class_name('email').text
        self.assertEqual('edith@mail.com', email)

        # she now checks what the carrot icon refers to:
        favorites = self.browser.find_element_by_class_name('favorites')
        favorites.click()
        self.assertIn('Mes Favoris', self.browser.title)
        favorites = self.browser.find_element_by_class_name('no-fav').text
        self.assertEqual(
            "Vous n'avez enregistré aucun favori pour le moment.",
            favorites)

        # For now, she logs out
        logout  = self.browser.find_element_by_class_name('logout')
        logout.click()
        self.assertIn('Pur Beurre', self.browser.title)

        # She comes back later, and wants to try to same some product :
        login  = self.browser.find_element_by_class_name('login')
        login.click()

        # she logs in with her username and password :
        username = self.browser.find_element_by_name('username')
        username.send_keys('Edith')
        password = self.browser.find_element_by_name('password')
        password.send_keys('Edithpassword')
        button = self.browser.find_element_by_tag_name('button')
        button.click()

        # she is sent back to the home page :
        self.assertIn('Pur Beurre', self.browser.title)

        # She searches a product :
        query = self.browser.find_element_by_id('input-home')
        query.send_keys('nutella')
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        
        # Edith verifies that the correctly landed on the search page
        self.assertIn('Recherche', self.browser.title)
        query_name = self.browser.find_element_by_class_name('query-name').text
        # And that the product she searched is faithful to her search
        self.assertEqual('nutella', query_name.lower())

        # she selects a product to replace the one she searched :
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        button = self.browser.find_element_by_id('ersatz_nutella_4')
        button.click()

        # Edith is now redirected to the favourites pages
        self.assertIn('Mes Favoris', self.browser.title)

        # she can asseses that the product she chose to replace nutella has
        # been properly saved
        product = self.browser.find_element_by_id('ersatz_nutella_4').text
        self.assertEqual('ersatz_nutella_4', product)

    def test_malicious_user(self):
        # Evil Edith has heard about a website called Pur Beurre,
        # she decides to visit it
        self.browser.get(self.live_server_url)

        # She decides to test the signup page :
        self.visit_signup_page()
        
        # She tries to login with indicating an email:
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('Edith')
        password1_input = self.browser.find_element_by_name('password1')
        password1_input.send_keys('Edithpassword')
        password2_input = self.browser.find_element_by_name('password2')
        password2_input.send_keys('Edithpassword')
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        # Thankfully, nothing happens :
        self.assertIn('Inscription', self.browser.title)

        # She tries to login with indicating a username:
        self.visit_signup_page()
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys('edith@mail.com')
        password1_input = self.browser.find_element_by_name('password1')
        password1_input.send_keys('Edithpassword')
        password2_input = self.browser.find_element_by_name('password2')
        password2_input.send_keys('Edithpassword')
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        # Thankfully, nothing happens :
        self.assertIn('Inscription', self.browser.title)

        # Same thing if the passwords do not match :
        self.visit_signup_page()
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('Edith')
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys('edith@mail.com')
        password1_input = self.browser.find_element_by_name('password1')
        password1_input.send_keys('Edithpassword')
        password2_input = self.browser.find_element_by_name('password2')
        password2_input.send_keys('Edith')
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        # Thankfully, nothing happens :
        self.assertIn('Inscription', self.browser.title)

        # Evil Edith gives in and correctly writes her coordinates
        self.visit_signup_page()
        username_input = self.browser.find_element_by_name('username')
        username_input.send_keys('Edith')
        email_input = self.browser.find_element_by_name('email')
        email_input.send_keys('edith@mail.com')
        password1_input = self.browser.find_element_by_name('password1')
        password1_input.send_keys('Edithpassword')
        password2_input = self.browser.find_element_by_name('password2')
        password2_input.send_keys('Edithpassword')
        button = self.browser.find_element_by_tag_name('button')
        button.click()

        # She tries to login with a different password than the one
        # she set earlier :
        logout  = self.browser.find_element_by_class_name('logout')
        logout.click()
        login = self.browser.find_element_by_class_name('login')
        login.click()
        self.assertIn('Connexion', self.browser.title)

        # She tries first a bad password :
        username = self.browser.find_element_by_name('username')
        username.send_keys('Edith')
        password = self.browser.find_element_by_name('password')
        password.send_keys('Edith')
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        # Thankfully, nothing happens :
        error_message = self.browser.find_element_by_class_name('errorlist').text
        self.assertEqual(error_message, "Saisissez un nom d'utilisateur et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).")

        # she finally tries with the right password but a false username :
        login = self.browser.find_element_by_class_name('login')
        login.click()
        username = self.browser.find_element_by_name('username')
        username.send_keys('irhuzear')
        password = self.browser.find_element_by_name('password')
        password.send_keys('Edithpassword')
        button = self.browser.find_element_by_tag_name('button')
        button.click()
        # Thankfully, nothing happens :
        error_message = self.browser.find_element_by_class_name('errorlist').text
        self.assertEqual(error_message, "Saisissez un nom d'utilisateur et un mot de passe valides. Remarquez que chacun de ces champs est sensible à la casse (différenciation des majuscules/minuscules).")

        # Disappointed, she leaves, this website was a too big target for her...
