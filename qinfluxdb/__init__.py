from influxdb.client import InfluxDBClient


class Client(InfluxDBClient):
    @property
    def q(self):
        return Query(client=self)


class Query(object):
    _clause_mappings = {
            'values': ', '.join,
            'series': str,
            'where': str,
            'group_by': ', '.join,
            'limit': str,
            'into': str,
            }

    def __init__(self, query=None, client=None):
        self.query = {} if query is None else query
        self.query.setdefault('values', '*')
        self.client = client
        self.columns = None

    def _clone(self, **kwargs):
        copy = self.__class__(self.query.copy(), self.client)
        copy.query.update(kwargs)
        return copy

    def _build_clauses(self, query):
        clauses = {}
        for clause in 'values', 'series':
            mapping = self._clause_mappings[clause]
            clauses[clause] = mapping(query[clause])
        for clause in 'where', 'group_by', 'limit', 'into':
            if clause in query:
                mapping = self._clause_mappings[clause]
                clauses[clause] = mapping(query[clause])
        return clauses

    def _build(self):
        clauses = self._build_clauses(self.query)
        base = 'select {values} from {series}'.format(**clauses)
        extensions = []
        if 'where' in self.query:
            extensions.append('where {where}'.format(**clauses))
        if 'group_by' in self.query:
            extensions.append('group by {group_by}'.format(**clauses))
        if 'limit' in self.query:
            extensions.append('limit {limit}'.format(**clauses))
        if 'into' in self.query:
            extensions.append('into {into}'.format(**clauses))
        query = ' '.join([base] + extensions)
        return query

    def __unicode__(self):
        return self._build()

    def __str__(self):
        return self._build()

    def values(self, *fields):
        return self._clone(values=fields)

    def from_series(self, series):
        return self._clone(series=series)

    def where(self, condition):
        if condition:
            return self._clone(where=condition)
        return self._clone()

    def group_by(self, *fields):
        return self._clone(group_by=fields)

    def limit(self, count):
        return self._clone(limit=count)

    def into(self, field):
        return self._clone(into=field)

    def _execute(self):
        response = self.client.query(str(self))
        if not response:
            raise StopIteration()
        response = response[0]
        columns = response['columns']
        yield columns
        for row in response['points']:
            obj = dict(zip(columns, row))
            yield obj

    def __iter__(self):
        response = self._execute()
        self.columns = next(response, [])
        return response

    def all(self):
        return list(iter(self))

    def first(self):
        return next(iter(self), None)




class Q(object):
    AND = 'and'
    OR = 'or'

    def __init__(self, queries=None, connection=None):
        self.queries = queries
        self.connection = connection

    def __and__(self, other):
        if self.queries is None:
            return other
        return Q([self, other], connection=self.AND)

    def __or__(self, other):
        if self.queries is None:
            return other
        return Q([self, other], connection=self.OR)

    def _build(self):
        if self.queries is None:
            return ''
        if not hasattr(self.queries, '__iter__'):
            return self.queries
        one, other = self.queries
        one = one._build()
        other = other._build()
        return '{one} {conn} {other}'.format(one=one, other=other,
                                            conn=self.connection)

    def __unicode__(self):
        return self._build()

    def __str__(self):
        return self._build()
