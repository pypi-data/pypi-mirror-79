from django.views.generic import ListView


class PaginatedListView(ListView):

    def pager_v2(self, rango=2):
        fin = int(self.object_list.__len__() / self.paginate_by)
        if self.object_list.__len__() / self.paginate_by > fin:
            fin += 1
        ini = 1
        page = self.request.GET.get('page', "1")
        if page.isdigit():
            page = int(page)
            ini = page - rango
            if ini <= 0:
                rango -= -1 + ini
                ini = 1
            if page + rango <= fin:
                fin = page + rango
            else:
                rango = (rango + page) - fin
                if ini - rango <= 0:
                    ini = 1
                else:
                    ini -= rango
        return range(ini, fin + 1)

    def get_context_data(self, **kwargs):
        context = super(PaginatedListView, self).get_context_data(**kwargs)
        page = self.request.GET.get("page", 1)
        context["current_page"] = int(page)
        pages = self.pager_v2(2)
        context["pages"] = pages
        return context
