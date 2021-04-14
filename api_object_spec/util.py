def flatten(collection):
    queue = [collection]
    items = []

    while queue:
        current = queue.pop()

        try:
            current_iter = iter(current)
        except TypeError:
            # Then this is terminal, so after appending it to items, we just want to
            # start on the next iterable in the collection
            items.append(current)

            continue
        try:
            c = current_iter.next()

             # We evidently haven't hit a StopIteration, so put the collection back on the queue.
            queue.append(current)

            # c is an item we want to return, so put it here.
            items.append(c)

            # c is also possible a collection, so put it on the queue of tasks to be completed. We're doing depth first, so put it on the end.
            queue.append(c)

        except StopIteration:
            # Simply don't put the current collection back on the queue.
            continue

    return items
