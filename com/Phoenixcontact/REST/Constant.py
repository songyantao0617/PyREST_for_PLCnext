class RestConstant(object):
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'

    CHARSET_UTF8 = 'UTF-8'
    BASE_URL = 'https://'
    HEADER_AUTH = 'Authorization'
    HEADER_BEARER = 'Bearer '
    HEADER_TYPE = 'Content-Type'
    HEADER_TYPE_JSON = 'application/json'
    HEADER_TYPE_TEXT = 'text/plain'

    TEMPORARY_TOCKEN_URI = '_pxc_api/auth/auth-token'
    TEMPORARY_TOCKEN_BODY_SCOPE_VALUES = 'variables'

    ACCESS_TOCKEN_URI = '_pxc_api/auth/access-token'

    REPORT_GROUP_URI = '_pxc_api/api/groups'
    REGISTER_GROUP_URI = '_pxc_api/api/groups'
    READ_GROUP_URI = '_pxc_api/api/groups/'
    # UNREGISTER_GROUP_URI = '_pxc_api/api/groups/'

    READ_VARIABLES_GET_URI = '_pxc_api/api/variables'
    WRITE_VARIABLES_PUT_URI = '_pxc_api/api/variables'

    SERVICE_DESCRIPTION_URI = '_pxc_api/api'

    # CREATE_SESSION_URI = '_pxc_api/api/sessions'
    CREATE_SESSION_URI = '_pxc_api/v1.1/sessions'

    # MAINTAIN_SESSION_URI = '_pxc_api/api/sessions/'
    MAINTAIN_SESSION_URI = '_pxc_api/v1.1/sessions/'

    SESSIONID = 'sessionID'
    REASSIGN_SESSION_URI = '_pxc_api/api/sessions/'
    REPORT_SESSIONS_URI = '_pxc_api/api/sessions'
    DELETE_SESSION_URI = '_pxc_api/api/sessions/'

    PATHPREFIX = 'Arp.Plc.Eclr/'
