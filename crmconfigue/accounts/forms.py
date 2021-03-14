from .models import Account
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields=("name","national_id", "economic_id", "email","phone","whatsapp_phone","office_phone", "fax",
         "industry","billing_address_line","billing_street","billing_city", "billing_state", "billing_postcode",
         "billing_country", "website", "description", "is_active", "archive","success_measure", "main_challenges",
         "yearly_goal", "longterm_goal", "solution_expectation", "employee_count",
         "yearly_revenue", "customer_base", "want_purchase", "solution_catalyst", "competing_products", "feature_convince",
         "competitors_feature", "product_offer", "best_solution", "business_help", "active_socialnetworks", "active_groups",
         "information_source", "count_decisionmakers", "influential_descisionmakers", "stakeholders", "influence_decisionmakers")