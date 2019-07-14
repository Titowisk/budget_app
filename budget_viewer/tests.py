from django.test import TestCase

# Create your tests here.
from .forms import CategoryForm

# https://docs.djangoproject.com/en/2.2/ref/forms/api/#more-granular-output

class CategoryFormTest(TestCase):

    def setUp(self):
        pass
    
    def testHtmlForm(self):
        """
        <select name="category" class="custom-select" id="id_category">
            <option value="Entertainment">Lazer</option>

            <option value="Food">Alimentação</option>

            <option value="Supplies">Suprimentos</option>

            <option value="HealthCare">Saúde</option>

            <option value="Utilities">Utilidades</option>

            <option value="Education">Educação</option>

            <option value="Transportation">Transporte</option>

            <option value="Clothing">Vestimenta</option>

        </select>
        """
        form = CategoryForm()
        print(form['category'])

        html_select = str(form['category'])
        self.assertGreaterEqual(html_select.find('<select'), 0) # form['category'] holds the <select> built from django forms
        self.assertGreaterEqual(html_select.find('<option'), 0)
