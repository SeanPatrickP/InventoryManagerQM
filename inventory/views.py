from django.shortcuts import render
from django.http import HttpResponse
from .models import Item, ProductIdCount, Sale
from django.template import loader
from decimal import Decimal
from django.http import QueryDict
import json

def index(request):
    items = parseItems()
    template = loader.get_template('inventory/home.html')

    context = {
        'items': items,
    }
    return HttpResponse(template.render(context, request))

def getItems(request):
    items = parseItems()
    template = loader.get_template('inventory/stockCheck.html')

    context = {
        'items': items,
    }
    return HttpResponse(template.render(context, request))

def getTotal():
    total = Sale(total=0.00)
    total.save()
    return parseTotal(total)

def parseTotal(total):
    return {
        'total': total.total,
        'total_products': total.products,
        'items': parseItems(),
        'saleId': total.id,
    }

def mapItemToSchema(item):
    return {
        'price': item.price,
        'description': item.description,
        'quantity': item.quantity,
        'productId': item.productId,
    }

def sellItems(request):
    context = getTotal()
    template = loader.get_template('inventory/sellItems.html')

    return HttpResponse(template.render(context, request))

def addItem(request):
    template = loader.get_template('inventory/addItem.html')

    context = {
        'productId' : getItemsCountRaw(),
    }
    return HttpResponse(template.render(context, request))

def deleteItem(request):
    productId = request.GET
    productId = str(productId.get('productId'))
    toDelete = Item.objects.get(productId=productId)

    response = {
        'status': 'not deleted',
    }

    if(toDelete):
        toDelete.delete()

        response = {
            'status': 'deleted',
            'productId': productId,
        }
    return HttpResponse(json.dumps(response))

def addItemToSell(request):
    get = request.GET
    productId = str(get.get('productId'))
    saleId = str(get.get('saleId'))
    sale = Sale.objects.get(id=saleId)
    toSell = Item.objects.get(productId=productId)
    sale.products.add(toSell)
    sale.total = sale.total + toSell.price
    sale.save()

    response = {
        'status': 'sold',
        'price': str(sale.total),
    }
    return HttpResponse(json.dumps(response))

def getItemsCount(request):
    allCounter = getItemsCountRaw()
    return(HttpResponse(allCounter)
)

def getItemsCountRaw():
    countObject = ProductIdCount.objects.get(countType="allProductIdTracker")
    return(countObject.count + 1)

def increaseCounts():
    countObject = ProductIdCount.objects.get(countType="allProductIdTracker")
    countObject.count += 1
    countObject.save()

def insertItem(request):
    data = QueryDict(request.body)
    productId = data.get('productId')
    quantity = data.get('quantity')
    price = data.get('price')
    description = data.get('description')
    newItem = Item(price=price, description=description, quantity=quantity, productId=productId)
    try: newItem.save()
    except: return HttpResponse(json.dumps({'status': 'not inserted'}))

    increaseCounts()

    response = {
        'status': 'inserted',
    }
    return HttpResponse(json.dumps(response))

def updateItem(request):
    data = QueryDict(request.body)
    productId = data.get('productId')
    quantity = data.get('quantity')
    price = data.get('price')
    toUpdate = Item.objects.get(productId=productId)

    response = {
        'status': 'not updated',
    }

    if(toUpdate):
        toUpdate.price = price
        toUpdate.quantity = quantity
        toUpdate.save()

        response = {
            'status': 'updated',
            'productId': productId,
        }
    return HttpResponse(json.dumps(response))

def sellSelected(request):
    data = QueryDict(request.body)
    saleId = data.get('saleId')
    saleObject = Sale.objects.get(id=saleId)
    saleProducts = saleObject.products.all()
    returnArr = []
    for saleProduct in saleProducts:
        saleProduct.quantity = saleProduct.quantity - 1
        saleProduct.save()
        returnArr.append({'productId': saleProduct.productId, 'quantity': saleProduct.quantity})
    
    response = {
            'status': 'sold',
            'itemsUpdated': returnArr,
    }
    return HttpResponse(json.dumps(response))

def parseItems():
    items = Item.objects.all()
    returnItems = []
    for item in items:
        mapped = mapItemToSchema(item)
        returnItems.append(mapped)

    return returnItems

def mapItemToSchema(item):
    return {
        'price': item.price,
        'description': item.description,
        'quantity': item.quantity,
        'productId': item.productId,
    }

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)