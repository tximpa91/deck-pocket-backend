class AuthorizationMiddleware(object):

    def resolve(self, next, root, info, **args):
        return next(root, info, **args)
