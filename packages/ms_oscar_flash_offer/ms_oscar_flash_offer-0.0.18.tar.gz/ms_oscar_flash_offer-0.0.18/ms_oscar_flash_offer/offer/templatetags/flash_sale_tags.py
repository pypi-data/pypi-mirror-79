from django import template


from .. import utils


register = template.Library()


@register.simple_tag
def is_product_on_sale(product):
    return utils.is_product_on_sale(product)


@register.simple_tag
def calculate_product_price_incl_discounts(product, price_data):
    return utils.calculate_product_price_incl_discounts(product, price_data)


@register.simple_tag
def get_flash_sale_offer(product):
    return utils.get_flash_sale_offer(product)
