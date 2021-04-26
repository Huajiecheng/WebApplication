from project.models import Order, Cart, CartEntry, OrderEntry
from datetime import datetime
from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

def show_me_the_money(sender, **kwargs):
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
	    if ipn_obj.receiver_email != "sb-bqsrm3728573@business.example.com":
	        # Not a valid payment
	        print( "not valid" )
	        return
	    order_id = int(ipn_obj.invoice.split('-')[-1])
	    order = get_object_or_404(Order,id = order_id)
	    if (order.status!="INPROGRESS"):
	        order.status = "INPROGRESS"
	        order.order_time = datetime.now()
	        order.save()
	        cart = get_object_or_404(Cart, owner=order.customer)
	        CartEntry.objects.filter(cart=cart).delete()
	        print("payment done")
	    else:
	        print("repeat")
	    # ALSO: for the same reason, you need to check the amount
	    # received etc. are all what you expect.
	else:
	    print( "Payment not completed" )
print("start handler")
valid_ipn_received.connect(show_me_the_money)