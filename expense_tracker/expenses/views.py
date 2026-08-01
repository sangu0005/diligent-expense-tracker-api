from django.db.models import Sum
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/expenses/            -> list all expenses
    GET  /api/expenses/?category=X -> list expenses filtered by category
    POST /api/expenses/            -> create a new expense
    """
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        queryset = Expense.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
        return queryset


class ExpenseDetailView(generics.RetrieveDestroyAPIView):
    """
    GET    /api/expenses/<id>/ -> retrieve a single expense
    DELETE /api/expenses/<id>/ -> delete a single expense
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class ExpenseTotalView(APIView):
    """
    GET /api/expenses/total/            -> overall total + breakdown by category
    GET /api/expenses/total/?category=X -> total for a single category
    """

    def get(self, request):
        category = request.query_params.get('category')

        if category:
            queryset = Expense.objects.filter(category__iexact=category)
            total = queryset.aggregate(total=Sum('amount'))['total'] or 0
            return Response({
                'category': category,
                'total': total,
            })

        overall_total = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        by_category_qs = (
            Expense.objects.values('category')
            .annotate(total=Sum('amount'))
            .order_by('category')
        )
        by_category = {row['category']: row['total'] for row in by_category_qs}

        return Response({
            'overall_total': overall_total,
            'by_category': by_category,
        })
