
from django.urls import path
from OCR.views.documentviews import ocr_data
from OCR.views.documentviews import index
from OCR.views.downloadCSV import download_csv

urlpatterns = [
    path('document',ocr_data ),
    path('esp', index),
    path('download',download_csv)
]
