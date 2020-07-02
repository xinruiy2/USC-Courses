from flask import Flask, request
import requests


app = Flask(__name__, static_url_path = '')
@app.route('/')
def root():
    return app.send_static_file("main.html")


@app.route("/second", methods = ['GET'])
def getvalue():
    keywords = "&keywords="+ str(request.args.get('fname'))
    counter = 0

    sorted_order = ""
    sortb = request.args.get('sortby')
    if sortb == "Best Match":
        sorted_order = "&sortOrder=" + "BestMatch"
    elif sortb == "Price: highest first":
        sorted_order = "&sortOrder=" + "CurrentPriceHighest"
    elif sortb == "Price + Shipping: highest first":
        sorted_order = "&sortOrder=" + "PricePlusShippingHighest"
    else:
        sorted_order = "&sortOrder=" + "PricePlusShippingLowest"

    max_price = ""
    maxprice = request.args.get('maxprice')
    if maxprice != "":
        max_price = "&itemFilter(" + str(counter) + ").name=MaxPrice" + "&itemFilter(" + str(counter) + ").value=" + str(maxprice) + "&itemFilter(" + str(counter) + ").paramName=Currency&itemFilter(" + str(counter) + ").paramValue=USD"
        counter += 1


    min_price = ""
    minprice = request.args.get('minprice')
    if minprice != "":
        min_price = "&itemFilter(" + str(counter) + ").name=MinPrice" + "&itemFilter(" + str(counter) + ").value=" + str(minprice) + "&itemFilter(" + str(counter) + ").paramName=Currency&itemFilter(" + str(counter) + ").paramValue=USD"
        counter += 1


    return_accept = ""
    return_accept_value = request.args.get('Return')
    # print(return_accept_value)
    if return_accept_value != None:
        return_accept = "&itemFilter(" + str(counter) + ").name=ReturnsAcceptedOnly&itemFilter(" + str(counter) + ").value=true"
        counter += 1

    freeShipping = ""
    shipping_Type = ""
    shipping_value1 = request.args.get('Free')
    shipping_value2 = request.args.get('Expedited')
    # print(shipping_value2)
    if shipping_value1 != None:
        freeShipping = "&itemFilter(" + str(counter) + ").name=FreeShippingOnly&itemFilter(" + str(counter) + ").value=true"
        counter += 1
    if shipping_value2 != None:
        shipping_Type = "&itemFilter(" + str(counter) + ").name=ExpeditedShippingType&itemFilter(" + str(counter) + ").value=Expedited"
        counter += 1

    condition = ""
    count = 0
    first = 0
    condition_new = request.args.get('New')
    condition_used = request.args.get('Used')
    condition_verygood = request.args.get('VeryGood')
    condition_good = request.args.get('Good')
    condition_acceptable = request.args.get('Acceptable')
    # print(condition_verygood)
    if condition_new != None:
        if first == 0:
            condition += "&itemFilter(" + str(counter) + ").name=Condition"
            first = 1
        condition += "&itemFilter(" + str(counter) + ").value(" + str(count) + ")=1000"
        count += 1
    if condition_used != None:
        if first == 0:
            condition += "&itemFilter(" + str(counter) + ").name=Condition"
            first = 1
        condition += "&itemFilter(" + str(counter) + ").value(" + str(count) + ")=3000"
        count += 1
    if condition_verygood != None:
        if first == 0:
            condition += "&itemFilter(" + str(counter) + ").name=Condition"
            first = 1
        condition += "&itemFilter(" + str(counter) + ").value(" + str(count) + ")=4000"
        count += 1
    if condition_good != None:
        if first == 0:
            condition += "&itemFilter(" + str(counter) + ").name=Condition"
            first = 1
        condition += "&itemFilter(" + str(counter) + ").value(" + str(count) + ")=5000"
        count += 1
    if condition_acceptable != None:
        if first == 0:
            condition += "&itemFilter(" + str(counter) + ").name=Condition"
            first = 1
        condition += "&itemFilter(" + str(counter) + ").value(" + str(count) + ")=6000"
        count += 1


    per_page  = "&paginationInput.entriesPerPage=15"

    base_url = "https://svcs.ebay.com/services/search/FindingService/v1?" \
     "OPERATION-NAME=findItemsAdvanced&" \
     "SERVICE-VERSION=1.0.0&"  \
     "SECURITY-APPNAME=XinruiYi-571proje-PRD-22eae7200-0aaa1f3f&" \
     "RESPONSE-DATA-FORMAT=JSON&" \
     "REST-PAYLOAD"

    url = base_url + keywords + per_page + sorted_order + max_price + min_price + return_accept + freeShipping + shipping_Type + condition
    r = requests.get(url)
    print(url)
    return r.text

if __name__ == '__main__':
    app.run(debug = True)
