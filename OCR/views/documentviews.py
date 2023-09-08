from email import message
from ftplib import error_temp
from http.client import HTTPResponse
from OCR.data_collection.special_doc_data_collection import specific_doc
from OCR.data_collection.PDF_doc_data_collection import document_data
from OCR.helpers.get_similarity import text_to_vector,get_cosine
import pandas as pd
from OCR.helpers.pdf_to_image import convert_pdf_in_images
from rest_framework.decorators import api_view
from rest_framework.response import Response
from OCR.serializers import ImagePathSerializer
from rest_framework import status
from django.http import JsonResponse
from django.shortcuts import render

@api_view(http_method_names=["POST"])
def ocr_data(request):
    # return Response(data={"message" : "CSV Created Successfully"}) 
    serializer = ImagePathSerializer(data=request.data)
    if serializer.is_valid():
        my_doc_path = serializer.validated_data.get("document_path")
        specific_doc_path = serializer.validated_data.get("specific_path")


        try:
            document_df=document_data(my_doc_path)
            specific_df=specific_doc(specific_doc_path)
        except Exception as error:
            return JsonResponse({"message" : str(error)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)      

        try:    
            final_df = pd.DataFrame()
            lookup = {}
            seen = set()

            # resetting index of dataframe as the index were not in sequence
            
            specific_df_cpy = specific_df.copy()
            specific_df_cpy.reset_index(inplace = True, drop = True)

            document_df_cpy = document_df.copy()
            document_df_cpy.reset_index(inplace = True, drop = True)

            for i, row in document_df_cpy.iterrows():
                
                my_doc_row = row
                row = row.to_list()
                my_doc_key = row[1]
                my_doc_val = row[2]

                for j, row in specific_df_cpy.iterrows():
                    specific_doc_row = row
                    row = row.to_list()
                    specif_doc_key = row[1]
                    specific_doc_val = row[2]
                    specific_vector = text_to_vector(str(specific_doc_val))
                    my_doc_vector = text_to_vector(str(my_doc_val))

                    match_percent = get_cosine(specific_vector, my_doc_vector)
                    if match_percent >= .5 and j not in seen:
                        percent= pd.DataFrame([match_percent*100])
                        if i not in lookup: 
                            lookup[i] = {"row": pd.concat([my_doc_row,specific_doc_row,percent],axis=0,ignore_index=True), "match_percent": match_percent}
                        else:
                            if lookup[i]["match_percent"] < match_percent:
                                lookup[i] = {"row": pd.concat([my_doc_row,specific_doc_row,percent],axis=0,ignore_index=True), "match_percent": match_percent}
                        seen.add(j)

            #concatinate rows in dataframe
            for k, v in lookup.items():
                final_df = pd.concat([final_df, v["row"]], axis=1, ignore_index=True)

            final_data_df=final_df.T.drop(columns=[0,3,6])
            final_data_df.columns=["Tender Parameter","Tender Requirments","Specific parameter","Specific Requirments","Match Percentage"]
            final_data_df.index = final_data_df.index+1
            final_data_df.index.name = " Sno."
            csv_data=final_data_df.to_csv("final_api_test.csv")

            return JsonResponse({"message" : "CSV Created Successfully"},status=status.HTTP_200_OK) 
        except Exception as error:
            return JsonResponse({"message":str(error)},status=status.HTTP_400_BAD_REQUEST)     
    else :
        return JsonResponse({"message" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)    

def index(request):
    return render(request,'font.html')