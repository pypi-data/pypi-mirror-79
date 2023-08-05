from itertools import chain
from save_to_db.core.item_base import ItemBase
from save_to_db.exceptions import ItemsNotTheSame


def merge_items(top_item, cls_items, cls_default_items, all_items):
    """Merges items that pull the same model from the database into a single
    items.

    :param top_item: the item that is being processed.
    :param items: List of items in which items referring to the same model
        must be merged.
    :param all_items: all single items in structure.
    """

    all_cls_items = cls_items[:]
    all_cls_items.extend(cls_default_items)

    merged_items = []
    item_to_merged = []
    while True:
        for item in all_cls_items:
            item_merged = False

            if item in merged_items or not item.getters:
                continue

            for group in item.getters:

                use_group = True
                for field_name in group:
                    if field_name not in item.data:
                        use_group = False
                        break
                if not use_group:
                    continue

                for next_item in all_cls_items:
                    if next_item is item or next_item in merged_items:
                        continue

                    do_merge = True
                    for key in group:
                        if (
                            key not in next_item
                            or (
                                not isinstance(item[key], ItemBase)
                                and item[key] != next_item[key]
                            )
                            or (
                                isinstance(item[key], ItemBase)
                                and not __same_items(item[key], next_item[key])
                            )
                        ):
                            do_merge = False
                            break

                    if not do_merge:
                        continue

                    __merge_item_into_item(item, next_item)
                    merged_items.append(next_item)
                    item_to_merged.append([item, next_item])
                    item_merged = True

            if item_merged:
                break

        # replacing merged_items with the extended item in single items
        for _, merged_item in item_to_merged:
            for one_item in all_items:
                for key, value in one_item.data.items():
                    if value is merged_item:
                        one_item[key] = item

            all_cls_items.remove(merged_item)
            if merged_item in cls_items:
                cls_items.remove(merged_item)

        # replacing in bulk items
        __replace_in_bulk_items(top_item, item_to_merged, processed_items=[])

        merged_items.clear()
        item_to_merged.clear()

        if not item_merged:
            break


def __replace_in_bulk_items(item, item_to_merged, processed_items):
    if item in processed_items:
        return
    processed_items.append(item)

    if item.is_single_item():
        for f_key, relation in item.relations.items():
            if f_key not in item or not relation["relation_type"].is_x_to_many():
                continue
            __replace_in_bulk_items(
                item[f_key], item_to_merged, processed_items=processed_items
            )
    else:
        for extened_item, merged_item in item_to_merged:
            if merged_item in item:
                index = item.bulk.index(merged_item)
                item.remove(merged_item)
                item.add_at_index(index, extened_item)

            # updating defaults
            for key, default_value in item.data.items():
                if not isinstance(default_value, ItemBase):
                    continue

                if default_value is merged_item:
                    item[key] = extened_item

                if default_value.is_bulk_item():
                    __replace_in_bulk_items(
                        default_value, item_to_merged, processed_items=processed_items
                    )

        for item_in_bulk in item:
            __replace_in_bulk_items(
                item_in_bulk, item_to_merged, processed_items=processed_items
            )


def __same_items(item_one, item_two, _no_check_pairs=None):
    if item_one.is_bulk_item():
        return True

    _no_check_pairs = _no_check_pairs or []

    for key in set(chain(item_one.data.keys(), item_two.data.keys())):
        if key not in item_one.data or key not in item_two.data:
            continue

        if (
            key in item_one.relations
            and item_one.relations[key]["relation_type"].is_x_to_many()
        ):
            continue

        if (
            key not in item_one.data
            or key not in item_two.data
            or item_two.data[key] != item_one.data[key]
        ):

            if key in item_one.relations:
                pair = [item_one, item_two]
                if pair in _no_check_pairs:
                    continue
                _no_check_pairs.append(pair)
                if type(item_one.data[key]).allow_merge_items:
                    if __same_items(
                        item_one.data[key],
                        item_two.data[key],
                        _no_check_pairs=_no_check_pairs,
                    ):
                        continue
            return False

    return True


def __merge_item_into_item(extended_item, merged_item):
    if not __same_items(extended_item, merged_item):
        raise ItemsNotTheSame(extended_item, merged_item)

    for key in merged_item.data:
        is_x_to_many = False
        if key in extended_item.relations:
            is_x_to_many = extended_item.relations[key]["relation_type"].is_x_to_many()

        if not is_x_to_many:
            if key not in extended_item.data:
                extended_item[key] = merged_item[key]
        else:
            for item in merged_item[key].bulk:
                extended_item[key].add(item)
