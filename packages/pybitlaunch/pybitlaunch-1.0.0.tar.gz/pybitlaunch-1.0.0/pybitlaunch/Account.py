from .BaseAPI import BaseAPI

# Account object service to handle object functions
class AccountService(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(AccountService, self).__init__(*args, **kwargs)

    # Show account information
    def Show(self):
        # Get data from API
        data = self.getData("user")
        return data
