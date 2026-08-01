from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Expense


class ExpenseAPITests(APITestCase):

    def setUp(self):
        self.food_expense = Expense.objects.create(
            title="Groceries", amount=Decimal("50.00"), category="Food", date="2026-07-01"
        )
        self.transport_expense = Expense.objects.create(
            title="Bus pass", amount=Decimal("30.00"), category="Transport", date="2026-07-02"
        )
        self.list_url = reverse('expense-list-create')
        self.total_url = reverse('expense-total')

    def test_create_expense(self):
        payload = {
            "title": "Coffee",
            "amount": "4.50",
            "category": "Food",
            "date": "2026-07-03",
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 3)

    def test_create_expense_rejects_non_positive_amount(self):
        payload = {
            "title": "Refund",
            "amount": "0",
            "category": "Food",
            "date": "2026-07-03",
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_expenses(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_category(self):
        response = self.client.get(self.list_url, {'category': 'Food'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Groceries')

    def test_filter_by_category_is_case_insensitive(self):
        response = self.client.get(self.list_url, {'category': 'food'})
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_expense(self):
        url = reverse('expense-detail', args=[self.food_expense.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Groceries')

    def test_retrieve_missing_expense_returns_404(self):
        url = reverse('expense-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_expense(self):
        url = reverse('expense-detail', args=[self.food_expense.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 1)

    def test_overall_total_and_breakdown(self):
        response = self.client.get(self.total_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(str(response.data['overall_total'])), Decimal("80.00"))
        self.assertEqual(Decimal(str(response.data['by_category']['Food'])), Decimal("50.00"))
        self.assertEqual(Decimal(str(response.data['by_category']['Transport'])), Decimal("30.00"))

    def test_total_filtered_by_category(self):
        response = self.client.get(self.total_url, {'category': 'Transport'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(str(response.data['total'])), Decimal("30.00"))

    def test_total_for_category_with_no_expenses_is_zero(self):
        response = self.client.get(self.total_url, {'category': 'Entertainment'})
        self.assertEqual(Decimal(str(response.data['total'])), Decimal("0"))
