import json

from future.backports.urllib.parse import parse_qs

from odoo import http
from odoo.http import request


# The (valid_request) method is a helper function that standardizes your API responses.
def valid_request(data,status):
    response_body = {
        'message' : 'done',
        'data' : data
    }
    return request.make_json_response(response_body,status=status)

def invalid_request(error,status):
    response_body = {
        'error' : error
    }
    return request.make_json_response(response_body,status=status)


# API Operations Naser (67)
class PropertyApi(http.Controller):

    @http.route("https://webservice.logixerp.com/webservice/v2/CreateWaybill?secureKey=A049E85FB20843CEA981CA6A281E7DA8", methods=["POST"], type="json", auth="none", csrf=False)
    def post_property_json(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)

        # The below to check if there is an error during create record at my database
        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                # When I use type json I don`t need (request.make_json_response) to handel sending data
                return {
                    "message": "Property has been create",
                    "id": res.id,
                    "name": res.name
                }
        except Exception as error:
            return {
                "message": error,
            }
