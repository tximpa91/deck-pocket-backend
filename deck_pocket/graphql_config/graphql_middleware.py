from promise import is_thenable


class Depromise(object):

    def resolve(self, next, root, info, **args):
        result = next(root, info, **args)
        if info.operation.operation == 'subscription' and is_thenable(result):
            return result.get()
        return result
