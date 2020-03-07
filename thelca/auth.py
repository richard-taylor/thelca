from thelca.error import NotAuthorisedError

class Authority:
    '''
    This is the interface to an OpenID service like keycloak.
    '''

    def check_create_item(self, token, dictionary):
        return self.user_id_from_token(token)

    def check_read_item(self, token, item):
        return self.user_id_from_token(token)

    def filter_readable_items(self, token, items):
        return (self.user_id_from_token(token), items)

    def check_update_item(self, token, current, proposed):
        return self.user_id_from_token(token)

    def check_create_link(self, token, dictionary):
        return self.user_id_from_token(token)

    def check_read_link(self, token, link):
        return self.user_id_from_token(token)

    def filter_readable_links(self, token, links):
        return (self.user_id_from_token(token), links)

    def check_update_link(self, token, current, proposed):
        return self.user_id_from_token(token)

    def check_delete_link(self, token, link):
        return self.user_id_from_token(token)

    def user_id_from_token(self, token):
        if token is None or token == 'BAAD':
            raise NotAuthorisedError()
        else:
            return "a-test-only-id-" + token
