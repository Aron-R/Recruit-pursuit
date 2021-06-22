from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.decorators import api_view

from ..documents import JobDocument
from ..forms import ApplyJobForm

# included
from ..models import *
from django.views import View
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

class HomeView(ListView):
    model = Job
    template_name = "home.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return self.model.objects.unfilled()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trendings"] = self.model.objects.unfilled(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(ListView):
    model = Job
    template_name = "jobs/search.html"
    context_object_name = "jobs"

    def get_queryset(self):
        # q = JobDocument.search().query("match", title=self.request.GET['position']).to_queryset()
        # print(q)
        # return q
        return self.model.objects.filter(
            location__contains=self.request.GET.get("location", ""),
            title__contains=self.request.GET.get("position", ""),
        )


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html"
    context_object_name = "jobs"
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = "jobs/details.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = "job_id"
    slug_url_kwarg = "job_id"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, "Successfully applied for the job!")
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy("jobs:home"))

    def get_success_url(self):
        return reverse_lazy("jobs:jobs-detail", kwargs={"id": self.kwargs["job_id"]})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs["job_id"])
        if applicant:
            messages.info(self.request, "You already applied for this job")
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


def favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={"auth": False, "status": "error"})

    job_id = request.POST.get("job_id")
    user_id = request.user.id
    try:
        fav = Favorite.objects.get(job_id=job_id, user_id=user_id, soft_deleted=False)
        if fav:
            fav.soft_deleted = True
            fav.save()
            # fav.delete()
            return JsonResponse(
                data={
                    "auth": True,
                    "status": "removed",
                    "message": "Job removed from your favorite list",
                }
            )
    except Favorite.DoesNotExist:
        Favorite.objects.create(job_id=job_id, user_id=user_id)
        return JsonResponse(
            data={
                "auth": True,
                "status": "added",
                "message": "Job added to your favorite list",
            }
        )


class uh(ListView):
    model = Freelancing_Job
    template_name = "jobs/freelancing.html"
    context_object_name = "jobs"
    paginate_by = 5

class uh2(DetailView):
    model = Freelancing_Job
    template_name = "jobs/details.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



def skillset(request):
    all_checker = Job.objects.all()
    paginator = Paginator(all_checker,10)
    page = request.GET.get('page')
    checkers = paginator.get_page(page)
    result = colors.objects.all()
    return render(request,'./skillsets.html',{"colors":result})

def skillsetResult(request):
    n = request.POST.getlist('checks')
    print(n)
    if (n):
        return render(request,'./skillsets-case1.html')
    # else:
    #     return redirect('./skillsets.html')
    return render(request,'./skillsets.html')

def render_skill(request):
    all_checker = Job.objects.all()
    paginator = Paginator(all_checker,10)
    page = request.GET.get('page')
    checkers = paginator.get_page(page)
    return render(request,'./skillsetResult-1.html')

# def saveGreySupplier(request):
#     q=request.POST.get("id")
#     # q = q.strip()
#     l=(request.POST.get("supplier_name"))

#     m=request.POST.get("address")
#     m = m.strip()
#     n=request.POST.get("city")
#     n = n.strip()
#     o=request.POST.get("contact_number")
#     o = o.strip()
#     p=request.POST.get("email")
#     p = p.strip()

#     r=request.POST.get("remarks")
#     r = r.strip()


#     try:
#         existing_quality=get_object_or_404(GreySuppliersMaster,id=q,supplier_name=l)
#         messages.error(request,"This supplier already exists")
#     except:
#         if  m=="" or n=="" or o=="" or p=="" or q=="" or l=="":
#             messages.error(request,"please enter valid input")
#             return redirect('masterGreySuppliers')
#         new_quality = GreySuppliersMaster(
#             id = q,
#             supplier_name = l,
#             city = n.upper(),
#             address = m.upper(),
#             email=p,
#             contact_number=o,
#             remarks=r.upper()

#         )
#         new_quality.save()
#         messages.success(request,"Supplier added")
#     return redirect('masterGreySuppliers')