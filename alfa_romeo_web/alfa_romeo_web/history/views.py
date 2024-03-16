from django.views import generic as views

from alfa_romeo_web.history.models import HistoryCategory, History


class HistoryCategoryView(views.ListView):
    model = HistoryCategory
    template_name = 'history/history_categories.html'


class DetailHistoryView(views.DetailView):
    model = History
    template_name = 'history/history_details.html'


# class ListHistoryView(views.ListView):
#     model = History
#     paginate_by = 8
#     template_name = 'history/history_listings.html'
#
#     def get_queryset(self):
#         category_id = self.request.GET.get('category')
#         # order_by = self.request.GET.get('order_by', 'year')
#
#         if category_id:
#             queryset = History.get_all_stories_by_categoryid(category_id)
#         else:
#             queryset = History.objects.all()
#
#         # if order_by == 'header':
#         #     queryset = queryset.order_by('header')
#         # else:
#         #     queryset = queryset.order_by('year')
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = HistoryCategory.get_all_categories()
#         for item in context['object_list']:
#             if item.category:
#                 item.category_name = item.category.name.strip()
#             else:
#                 item.category_name = None
#
#         # context['order_by'] = self.request.GET.get('order_by', 'contributors')
#
#         context['category_id'] = self.request.GET.get('category')
#
#         context['categories'] = categories
#         return context
