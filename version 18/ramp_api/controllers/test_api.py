from odoo import http


class TestApi(http.Controller):

    @http.route("/api/test",methods=["GET"],type="http",auth="none",csrf=False)
    # "/api/test" => end point : address when call Execute function (test_endpoint) => enter
    # Get method : related to read data
    def test_endpoint(self):
        print("inside test_endpoint method")