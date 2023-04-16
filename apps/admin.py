import csv
import io

from django.contrib import admin
from django.db.models import Model, Count, OneToOneField, CASCADE
from django.contrib.admin import AdminSite, ModelAdmin
from django.forms import forms, ModelForm, CharField, ModelChoiceField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.safestring import mark_safe

from apps.models import Product, Category, ProductProxy


# ikkita admin site yasash
class EventAdminSite(AdminSite):
    site_header = "Nusratullo"
    site_title = "Nusrat"
    index_title = "Welcome to Nusratullo's website"


event_admin_site = EventAdminSite(name='event_admin')


# bu yerda endi product uchun alohida admin sayt qiladi
# event_admin_site.register(Product)


# admin paneldan olib tashlash
# admin.site.unregister(Group)


# adminkani override qilish manashu linkda batafsil ko'rsatilgan
# https://docs.djangoproject.com/en/dev/ref/contrib/admin/#overriding-admin-templates


# modelni register qilish
# @admin.register(Product)
# class ProductAdminModel(ModelAdmin):
# productsni bosganimizda bizga databaseda bor productlarning name va descriptionnini chiqaradi
# list_display = ('name','description')

# product qo'shmoqchi bo'lsak yoki o'zimizda bor productni o'zgartirmoqchi bo'lsak faqat mana shu fieldlari chiqadi
# fields = ('name','description')

# exclude esa fields ni teskaris, faqat mana shu filedlar chiqmasin
# exclude = ('name','description')

# bu name_count deb atalgan model ichida o'zimiz qo'lda yozib qo'ygan bir method hisoblanadi
# list_display = ('name_count',)

# bu esa tepadagi methodni model.py ga emas balki admin.py ni o'ziga yozish
# def name_count(self,obj: Product):
#     return obj.name.count('p')

# nechta borligini topish
# def get_queryset(self, request):
#     queryset = super().get_queryset(request)
#     queryset = queryset.annotate(
#         _name_count=Count("name", distinct=True),
#         _description_count=Count("description", distinct=True),
#     )
#     return queryset
#
# def name_count(self, obj):
#     return obj._name_count
#
# def description_count(self, obj):
#     return obj._description_count
#
# list_display = ('name_count','description_count')

# agar price 5 dan katta bo'lsa True degan yozuv chiqadi aks holda False degan yozuv chiqadi
# def get_price(self, obj):
#     return obj.price > 5
# list_display = ('get_price',)

# websahifani o'ng tarafida filter degan joyida faqat name va pricelar chiqsin degani va birorta fieldini bossak o'shani filter qilib beradi
# list_filter = ('name','price')


# list_display = ('name', 'price', 'is_very_benevolent')
# def is_very_benevolent(self, obj):
#     return obj.price > 30

# mana bu narsa True False o'rniga ptichka va x chiqarib beradi
# is_very_benevolent.boolean = True


# action qo'shish ya'ni ma'lum bir vazifani bajaradigan tugma qo'shish
# actions = ['mark_immortal']
#
# def mark_immortal(self, request, queryset):
#     queryset.update(is_immortal=True)


# bu funksiya databasedagi ma'lumotlarni csv faylga yozib beradi ya'ni eksport qilib beradi.
# actions = ["export_as_csv"]
#
# def export_as_csv(self, request, queryset):
#     meta = self.model._meta
#     field_names = [field.name for field in meta.fields]
#
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
#     writer = csv.writer(response)
#
#     writer.writerow(field_names)
#     for obj in queryset:
#         row = writer.writerow([getattr(obj, field) for field in field_names])
#
#     return response


# export_as_csv.short_description = "Export Selected"


# actionni nomlarini olish va o'chirish
# def get_actions(self, request):
#     actions = super().get_actions(request)
#     if 'delete_selected' in actions:
#         del actions['delete_selected']
#     return actions


# databasega csv faylni yozish uchun kerak ya'ni mixin qilib ishlatamiz
# class ExportCsvMixin:
#     def export_as_csv(self, request, queryset):
#         meta = self.model._meta
#         field_names = [field.name for field in meta.fields]
#
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
#         writer = csv.writer(response)
#
#         writer.writerow(field_names)
#         for obj in queryset:
#             row = writer.writerow([getattr(obj, field) for field in field_names])
#
#         return response


# csv fayllar bilan ishlash uchun kerak
# class CsvImportForm(forms.Form):
#     csv_file = forms.FileField()


# csv faylni databsega yozish admin panel orqali
# @admin.register(Product)
# class TagModelAdmin(admin.ModelAdmin, ExportCsvMixin):
#     actions = ['export_as_csv']
#     change_list_template = "admin/change_list.html"
#
#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('import-csv/', self.import_csv),
#         ]
#         return my_urls + urls
#
#     def import_csv(self, request):
#         if request.method == "POST":
#             csv_file = request.FILES["csv_file"]
#             decoded_file = csv_file.read().decode('utf-8')
#             io_string = io.StringIO(decoded_file)
#             bulk = []
#             for row in csv.DictReader(io_string):
#                 row.pop('id')
#                 bulk.append(Product(**row))
#                 # Tag.objects.update_or_create(row, id=row['id'])
#                 # Tag.objects.create(id=row["id"], name=row["name"])
#             Product.objects.bulk_create(bulk)
#             self.message_user(request, "Your csv file has been imported")
#             return redirect("..")
#         form = CsvImportForm()
#         context = {
#             "form": form
#         }
#         return render(
#             request, 'admin/csv_form.html', context
#         )

# @admin.register(Category)
# class CategoryAdminModel(ModelAdmin):
#     pass


# bu funksiyani vazifasi bitta product qo'shgandan so'ng qo'shish tugmasi o'chib qoladi
# def has_add_permission(self, request):
#     MAX_OBJECTS = 1
#     if self.model.objects.count() >= MAX_OBJECTS:
#         return False
#     return super().has_add_permission(request)

# qo'shish tugmasini o'chirib qo'yamiz
# def has_add_permission(self, request):
#     return False

# delete tugmachasini o'chirib qo'yish
# def has_delete_permission(self, request, obj=None):
#     return False

# update qilaolmaydigan qilib qo'yish
# def has_change_permission(self, request, obj=None):
#     return False

# admin panelda Product modeli o'chib qoladi ya'ni unregisterga o'xshaydi
# def has_module_permission(self, request):
#     return False

# def has_view_permission(self, request, obj=None):
#     return False


# category qo'shayotganda unga qo'shib bir nechta bolasini ham qo'shish mumkin defaultda 3 ta bo'ladi.
# ko'paytirish va kamaytirish mumkin. Ustunma ketin  joylashtirib beradi
# class VillainInline(admin.StackedInline):
#     model = Product
#     max_num = 4

# @admin.register(Category)
# class ProductAdminModel(ModelAdmin):
#     inlines = [VillainInline]


# xuddi StackedInlinega o'xshaydi faqat bu TabularInline ustunma ketin emas yon tarafga qarab chiqaradi
# class VillainInline(admin.TabularInline):
#     model = Product
#     max_num = 2
# @admin.register(Category)
# class ProductAdminModel(ModelAdmin):
#     inlines = [VillainInline]


# bir ga bir bog'lanish orqali ma'lumot kiritish
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response


#
#
# class HeroAcquaintance(Model):
#     "Non family contacts of a Hero"
#     hero = OneToOneField(Category, on_delete=CASCADE)
#
#
# class HeroAcquaintanceInline(admin.TabularInline):
#     model = Product
#
#
# @admin.register(Category)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     inlines = [HeroAcquaintanceInline]


# product qo'shayotganda birdaniga categoryni nomini ham berib ketsak bo'ladi. Va shu product categoryni bolasi bo'ladi
# class HeroForm(ModelForm):
#     category_name = CharField()

# class Meta:
#     model = Product
#     exclude = ["category"]

# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     form = HeroForm

# def save_model(self, request, obj, form, change):
#     category_name = form.cleaned_data["category_name"]
#     category, _ = Category.objects.get_or_create(name=category_name)
#     obj.category = category
#     super().save_model(request, obj, form, change)


# pagenationga o'xshab ketadi agar list_per_page = 1 bo'lsa bitta product chiqadi va qolganlari pagination ko'rinishida chiqadi
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     list_per_page = 1

# django admin sahifalarini o'chirib qo'yish
# import sys
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     list_per_page = sys.maxsize


# sana chiqarish
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     date_hierarchy = 'created_at'


# Productlarni bolalari bilan qoshib chiqarish
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     list_display = ('children_display',)

#     def children_display(self, obj):
#         return ", ".join([
#             child.name for child in obj.children.all()
#         ])
#     children_display.short_description = "Children"


# productni rasmini ham chiqarish
# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     readonly_fields = ["botirjon"]
#
#     def botirjon(self, obj: Product):
#         head = obj.image
#         return mark_safe(f'<img src="{head.url}" width="200" height="200" />')


# faqat o'qish mumkin qo'shib o'zgartirib o'chirib bo'lmaydi
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     readonly_fields = ["name", "price"]


# fieldslar ko'rinmaydi faqat borligini bilasiz xolos
# @admin.register(Product)
# class ProductAdminModel(admin.ModelAdmin):
#     def get_readonly_fields(self, request, obj=None):
#         if obj:
#             return ["name", "price"]
#         else:
#             return []
#     list_display = ('get_readonly_fields',)


# product qo'shayotganimizda faqat biz bergan categorylarni nomi chiqadi va faqat shularga product qo'shaoladi
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "category":
#             kwargs["queryset"] = Category.objects.filter(name__in=['Technology', 'h'])
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# otasini ham ko'rsatib ketish
# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     raw_id_fields = ["category"]


# categoryni nomi bilan chiqarish
# class CategoryChoiceField(ModelChoiceField):
#     def label_from_instance(self, obj):
#         return obj.name
#
# @admin.register(Product)
# class ProductAdminModel(ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'category':
#             return CategoryChoiceField(queryset=Category.objects.all())
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# is_unique ni checkbox qo'yib beradi ya'ni qo'shayotganimzda button qo'yib beradi
# @admin.register(Product)
# class VillainAdmin(admin.ModelAdmin, ExportCsvMixin):
#     change_form_template = "change_form.html"


# def response_change(self, request, obj):
#     if "_make-unique" in request.POST:
#         matching_names_except_this = self.get_queryset(request).filter(name=obj.name).exclude(pk=obj.id)
#         matching_names_except_this.delete()
#         obj.is_unique = True
#         obj.save()
#         self.message_user(request, "This villain is now unique")
#         return HttpResponseRedirect(".")
#     return super().response_change(request, obj)



# @admin.register(Product)
# class HeroAdmin(admin.ModelAdmin, ExportCsvMixin):
#     def children_display(self, obj):
#         display_text = ", ".join([
#             "<a href={}>{}</a>".format(
#                 reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name),
#                         args=(child.pk,)),
#                 child.name)
#             for child in obj.children.all()
#         ])
#         if display_text:
#             return mark_safe(display_text)
#         return "-"


# bitta modelni ikki marta register qilish uchun proxy model yozish kerak
# admin.site.register(ProductProxy)
# admin.site.register(ProductProxy)
# @admin.register(ProductProxy)
# class HeroProxyAdmin(admin.ModelAdmin):
# pass


# nested inlineni admin panelni chiqarish uchun djangoda django packagedan foydalanish kerak
# @admin.register(Product)
# class ProductAdminModel(ModelAdmin):
#     list_display = ('save_model',)

# def save_model(self, request, obj, form, change):
#     obj.added_by = request.user
#     super().save_model(request, obj, form, change)





# raqamlarni qarab admin panelni sortirovka bilan chiqarish
# class ClientAdminSite(AdminSite):
#     site_header = "Client uchun adminka"
#     site_title = "Client Events Admin Portal"
#     index_title = "Welcome to Client Researcher Events Portal"
#     login_form = CustomAuthForm
#     login_template = 'admin/custom/custom_login.html'
#
#     def get_app_list(self, request, app_label=None):
#         """
#         Return a sorted list of all the installed apps that have been
#         registered in this site.
#         """
#
#         ordering = {
#             "Categories": 0,
#             'Heroes': 1,
#             "Products": 2,
#             "Entitys": 3,
#             "Origins": 4,
#             "Tags": 6,
#             "Groups": 1,
#             "Users": 2,
#         }
#         app_dict = self._build_app_dict(request)
#         # a.sort(key=lambda x: b.index(x[0]))
#         # Sort the apps alphabetically.
#         app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
#
#         # Sort the models alphabetically within each app.
#         for app in app_list:
#             app['models'].sort(key=lambda x: ordering[x['name']])
#
#         return app_list

# client_admin_site = ClientAdminSite(name='client_admin')





# order by ishlatgan holda sortirovka qilish. annotate - bu narsa modelni fieldi bo'lmagan narsani modelni fieldi o'xshab berib yuborish
# @admin.register(Origin, site=client_admin_site)
# class OriginAdmin(admin.ModelAdmin):
#     list_display = ('name', 'hero_count', 'villain_count')
#
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(
#             _hero_count=Count("hero", distinct=True),
#             _villain_count=Count("villain", distinct=True),
#         ).order_by('_hero_count', '_villain_count')
#         return queryset
#
#     def hero_count(self, obj):
#         return obj._hero_count
#
#     def villain_count(self, obj):
#         return obj._villain_count




