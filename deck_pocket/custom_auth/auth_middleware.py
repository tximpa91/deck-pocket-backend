class AuthorizationMiddleware(object):

    def resolve(self, next, root, info, **args):
        user = info.context.data.get('user')
        args['user'] = user
        return next(root, info, **args)
