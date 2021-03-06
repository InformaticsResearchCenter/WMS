from WMS.models import *


def avaibleItem(status, deleted, usergroup):
    avaibleItem = ItemData.objects.select_related('inbound').filter(
        status=status, deleted=deleted, userGroup=usergroup).values('inbound__item')
    rawitem = []
    for i in avaibleItem:
        found = False
        for a in rawitem:
            if i['inbound__item'] == a['item']:
                a['qty'] += 1
                found = True
                break
        if found == False:
            try:
                rawitem.append({'item': i['inbound__item'], 'name': Item.objects.filter(
                    id=i['inbound__item']).values('name')[0]['name'],'size': Item.objects.filter(
                    id=i['inbound__item']).values('size')[0]['size'], 'colour': Item.objects.filter(
                    id=i['inbound__item']).values('colour')[0]['colour'], 'qty': 1})
            except:
                pass

    borrowItem = BorrowData.objects.select_related('borrow').filter(
        deleted=deleted, borrow__status=2, userGroup=usergroup).values('item', 'quantity')
    outboundItem = OutboundData.objects.select_related('outbound').filter(
        deleted=deleted, outbound__status=2, userGroup=usergroup).values('item', 'quantity')
    costumerReturItem = CostumerReturnData.objects.select_related('costumerReturn').filter(
        deleted=deleted, costumerReturn__status=2, userGroup=usergroup).values('item',  'quantity')
    borrowItem1 = BorrowData.objects.select_related('borrow').filter(
        deleted=deleted, borrow__status=1, userGroup=usergroup).values('item', 'quantity')
    outboundItem1 = OutboundData.objects.select_related('outbound').filter(
        deleted=deleted, outbound__status=1, userGroup=usergroup).values('item', 'quantity')
    costumerReturItem1 = CostumerReturnData.objects.select_related('costumerReturn').filter(
        deleted=deleted, costumerReturn__status=1, userGroup=usergroup).values('item',  'quantity')
    

    for i in outboundItem:
        for a in rawitem:
            if a['item'] == i['item']:
                a['qty'] -= i['quantity']
                if a['qty'] <= 0:
                    a['qty'] = 0
                else:
                    pass

    for i in borrowItem:
        for a in rawitem:
            if a['item'] == i['item']:
                a['qty'] -= i['quantity']
                if a['qty'] <= 0:
                    a['qty'] = 0
                else:
                    pass

    for i in costumerReturItem:
        for a in rawitem:
            if a['item'] == i['item']:
                a['qty'] -= i['quantity']
                if a['qty'] <= 0:
                    a['qty'] = 0
                else:
                    pass

    for i in outboundItem1:
        for a in rawitem:
            if a['item'] == i['item']:
                a['qty'] -= i['quantity']
                if a['qty'] <= 0:
                    a['qty'] = 0
                else:
                    pass

    for i in borrowItem1:
        for a in rawitem:
            if a['item'] == i['item']:
                a['qty'] -= i['quantity']
                if a['qty'] <= 0:
                    a['qty'] = 0
                else:
                    pass

    for i in costumerReturItem1:
        for a in rawitem:
            if a['item'] == i['item']:
                a['qty'] -= i['quantity']
                if a['qty'] <= 0:
                    a['qty'] = 0
                else:
                    pass
    return rawitem
