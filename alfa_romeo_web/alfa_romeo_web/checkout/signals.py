# from django.dispatch import receiver
# from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
# from paypal.standard.models import ST_PP_COMPLETED
#
#
# @receiver(valid_ipn_received)
# def show_me_the_money(sender, **kwargs):
#     """Do things here upon a valid IPN message received"""
#     ipn_obj = sender
#     if ipn_obj.payment_status == ST_PP_COMPLETED:
#         print('working')
#     else:
#         print("not working")
#
#
# valid_ipn_received.connect(show_me_the_money)
#
#
# @receiver(invalid_ipn_received)
# def do_not_show_me_the_money(sender, **kwargs):
#     """Do things here upon an invalid IPN message received"""
#     print('failed payment')
