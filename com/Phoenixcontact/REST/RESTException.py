class RESTException(Exception):

    def __init__(self, message):
        Exception.__init__(self,message)
        self.message = message
#
# # try:
# #     raise RESTException("A RESTException!")  # 主动触发异常
# # except:
# #     print("GOD, A RESTException!")

# class RESTException(Exception):
#     """ Unspecified RESTException. """
#     def __init__(self, *args, **kwargs): # real signature unknown
#         pass
