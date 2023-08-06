from tastypie.paginator import Paginator


class SmartPaginator(Paginator):
    """
    Limits result sets down to sane amounts for passing to the client.

    This is used in place of Django's ``Paginator`` due to the way pagination
    works. ``limit`` & ``offset`` (tastypie) are used in place of ``page``
    (Django) so none of the page-related calculations are necessary.

    This implementation also provides additional details like the
    ``total_count`` of resources seen and convenience links to the
    ``previous``/``next`` pages of data as available.

    This implementation does not perform ``SELECT COUNT(*)`` when
    ``limit`` is 0 and ``offset`` is 0 or ``limit`` is greater than 0 and
    ``offset`` is 0 and length of ``self.objects``is lower than ``limit``.
    """
    def get_count(self, limit=None, offset=None):
        if (limit in (0, self.max_limit) and offset == 0):
            return len(list(self.objects))

        next_page = self.objects[offset + limit:offset + limit + 1]
        if (limit > 0 and offset == 0 and (next_page == [] or next_page.count() == 0)):
            return len(list(self.objects))

        return super(SmartPaginator, self).get_count()

    def page(self):
        limit = self.get_limit()
        offset = self.get_offset()
        count = self.get_count(limit=limit, offset=offset)
        objects = self.get_slice(limit, offset)
        meta = {
            'offset': offset,
            'limit': limit,
            'total_count': count,
        }

        if limit:
            meta['previous'] = self.get_previous(limit, offset)
            meta['next'] = self.get_next(limit, offset, count)

        return {
            self.collection_name: objects,
            'meta': meta,
        }
