from django.core.cache import cache

def get_item_from_cache(item_id):
    return cache.get(f'item_{item_id}')

def set_item_in_cache(item_id, item):
    cache.set(f'item_{item_id}', item, timeout=60 * 15)
